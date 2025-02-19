# -- BEGIN LICENSE BLOCK ----------------------------------------------
# -- END LICENSE BLOCK ------------------------------------------------
#
# ---------------------------------------------------------------------
# !\file
#
# \author  Melih Yazgan <yazgan@fzi.de>
# \date    2024-07-09
#
#
# ---------------------------------------------------------------------
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .its_pdu_header import ItsPduHeader

@dataclass
class PositionConfidenceEllipse:
    semiMajorConfidence: int = 0
    semiMinorConfidence: int = 0
    semiMajorOrientation: int = 0


@dataclass
class Altitude:
    altitudeValue: int = 0
    altitudeConfidence: int = 0


@dataclass
class ReferencePosition:
    latitude: float = 0.0
    longitude: float = 0.0
    positionConfidenceEllipse: PositionConfidenceEllipse = field(default_factory=PositionConfidenceEllipse)
    altitude: Altitude = field(default_factory=Altitude)


@dataclass
class XDistance:
    value: float = 0.0
    confidence: int = 0


@dataclass
class YDistance:
    value: float = 0.0
    confidence: int = 0


@dataclass
class ZDistance:
    value: float = 0.0
    confidence: int = 0


@dataclass
class XSpeed:
    value: float = 0.0
    confidence: int = 0


@dataclass
class YSpeed:
    value: float = 0.0
    confidence: int = 0


@dataclass
class ZSpeed:
    value: float = 0.0
    confidence: int = 0


@dataclass
class YawAngle:
    angleValue: float = 0.0
    confidence: float = 0.0


@dataclass
class DimensionPlanar:
    value: float = 0.0
    confidence: int = 0


@dataclass
class Classification:
    confidence: int = 0
    classificationType: str = ""


@dataclass
class MatchedPosition:
    laneId: int
    longitudinalLanePositionValue: float = 0.0
    longitudinalLanePositionConfidenceValue: int = 0


@dataclass
class CpmPerceivedObject:
    objectId: int = 0
    time_of_measurement: float = 0.0
    xDistance: XDistance = field(default_factory=XDistance)
    yDistance: YDistance = field(default_factory=YDistance)
    xSpeed: XSpeed = field(default_factory=XSpeed)
    ySpeed: YSpeed = field(default_factory=YSpeed)
    dimensionPlanar1: DimensionPlanar = field(default_factory=DimensionPlanar)
    dimensionPlanar2: DimensionPlanar = field(default_factory=DimensionPlanar)
    classification: Classification =    field(default_factory=Classification)
    zDistance: Optional[ZDistance] = None
    zSpeed: Optional[ZSpeed] = None
    yawAngle: Optional[YawAngle] = None
    dimensionVertical: Optional[DimensionPlanar] = None
    matchedPosition: Optional[MatchedPosition] = None
    
@dataclass
class ManagementContainer:
    stationType: int = 0
    referencePosition: ReferencePosition = field(default_factory=ReferencePosition)


@dataclass
class CpmParameters:
    numberOfPerceivedObjects: int = 0
    cpmPerceivedObjectContainer: List[CpmPerceivedObject] = field(default_factory=list)
    managementContainer: ManagementContainer = field(default_factory=ManagementContainer)


@dataclass
class CPM:
    header: ItsPduHeader = field(default_factory=lambda: ItsPduHeader(protocol_version=2, message_id=14, station_id=2))
    generationDeltaTime: int = 0
    cpmParameters: CpmParameters = field(default_factory=CpmParameters)

    @classmethod
    def from_dict(cls, data: Dict) -> "CPM":
        def decode_reference_position(data: Dict) -> ReferencePosition:
            position_confidence_ellipse = PositionConfidenceEllipse(
                semiMajorConfidence=data["positionConfidenceEllipse"]["semiMajorConfidence"],
                semiMinorConfidence=data["positionConfidenceEllipse"]["semiMinorConfidence"],
                semiMajorOrientation=data["positionConfidenceEllipse"]["semiMajorOrientation"]
            )
            altitude = Altitude(
                altitudeValue=data["altitude"]["altitudeValue"],
                altitudeConfidence=data["altitude"]["altitudeConfidence"]
            )
            return ReferencePosition(
                latitude=data["latitude"] * 1e-7,
                longitude=data["longitude"] * 1e-7,
                positionConfidenceEllipse=position_confidence_ellipse,
                altitude=altitude
            )

        def decode_cpm_perceived_object(data: Dict) -> CpmPerceivedObject:
            return CpmPerceivedObject(
                objectId=data["objectID"],
                time_of_measurement=data["timeOfMeasurement"],
                xDistance=XDistance(value=data["xDistance"]["value"]/100, confidence=data["xDistance"]["confidence"]),
                yDistance=YDistance(value=data["yDistance"]["value"]/100, confidence=data["yDistance"]["confidence"]),
                xSpeed=XSpeed(value=data["xSpeed"]["value"]/100, confidence=data["xSpeed"]["confidence"]),
                ySpeed=YSpeed(value=data["ySpeed"]["value"]/100, confidence=data["ySpeed"]["confidence"]),
                dimensionPlanar1=DimensionPlanar(value=data["planarObjectDimension1"]["value"]/100, confidence=data["planarObjectDimension1"]["confidence"]),
                dimensionPlanar2=DimensionPlanar(value=data["planarObjectDimension2"]["value"]/100, confidence=data["planarObjectDimension2"]["confidence"]),
                classification=Classification(confidence=data["classification"][0]["confidence"], classificationType=data["classification"][0]["class"][1]["type"]),
                matchedPosition=MatchedPosition(
                    laneId=data["matchedPosition"]["laneID"],
                    longitudinalLanePositionValue=data["matchedPosition"]["longitudinalLanePosition"]["longitudinalLanePositionValue"],
                    longitudinalLanePositionConfidenceValue=data["matchedPosition"]["longitudinalLanePosition"]["longitudinalLanePositionConfidence"]
                ) if "matchedPosition" in data else None
            )

        header = ItsPduHeader.from_dict(data.get("header", {}))
        generation_delta_time = data["cpm"].get("generationDeltaTime", 0)

        management_container = ManagementContainer(
            # itsContainerStationType=data["cpm"]["cpmParameters"]["managementContainer"]["itsContainerStationType"],
            referencePosition=decode_reference_position(data["cpm"]["cpmParameters"]["managementContainer"]["referencePosition"])
        )

        perceived_objects = [
            decode_cpm_perceived_object(obj) for obj in data["cpm"]["cpmParameters"]["perceivedObjectContainer"]
        ]

        cpm_parameters = CpmParameters(
            numberOfPerceivedObjects=data["cpm"]["cpmParameters"]["numberOfPerceivedObjects"],
            cpmPerceivedObjectContainer=perceived_objects,
            managementContainer=management_container
        )

        return cls(
            header=header,
            generationDeltaTime=generation_delta_time,
            cpmParameters=cpm_parameters
        )
    
    
    def to_dict(self) -> Dict:
        def encode_reference_position(position: ReferencePosition) -> Dict:
            return {
                "latitude": int(position.latitude * 1e7),  # Multiply back to original scale
                "longitude": int(position.longitude * 1e7),# Multiply back to original scale
                "positionConfidenceEllipse": {
                    "semiMajorConfidence": int(position.positionConfidenceEllipse.semiMajorConfidence),
                    "semiMinorConfidence": int(position.positionConfidenceEllipse.semiMinorConfidence),
                    "semiMajorOrientation": int(position.positionConfidenceEllipse.semiMajorOrientation),
                },
                "altitude": {
                    "altitudeValue": int(position.altitude.altitudeValue),
                    "altitudeConfidence": int(position.altitude.altitudeConfidence),
                }
            }

        def encode_cpm_perceived_object(obj: CpmPerceivedObject) -> Dict:
            encoded_obj = {
                "objectID": obj.objectId,
                "timeOfMeasurement": int(obj.time_of_measurement),
                "xDistance": int({"value": obj.xDistance.value * 100, "confidence": obj.xDistance.confidence}),# Multiply back to original scale
                "yDistance": int({"value": obj.yDistance.value * 100, "confidence": obj.yDistance.confidence}),# Multiply back to original scale
                "xSpeed": int({"value": obj.xSpeed.value * 100, "confidence": obj.xSpeed.confidence}),# Multiply back to original scale
                "ySpeed": int({"value": obj.ySpeed.value * 100, "confidence": obj.ySpeed.confidence}),# Multiply back to original scale
                "planarObjectDimension1": int({"value": obj.dimensionPlanar1.value * 100, "confidence": obj.dimensionPlanar1.confidence}),# Multiply back to original scale
                "planarObjectDimension2": int({"value": obj.dimensionPlanar2.value * 100, "confidence": obj.dimensionPlanar2.confidence}),# Multiply back to original scale
                "classification": [{"confidence": obj.classification.confidence, "class": [{"type": obj.classification.classificationType}]}],
            }
            if obj.matchedPosition:
                encoded_obj["matchedPosition"] = {
                    "laneID": obj.matchedPosition.laneId,
                    "longitudinalLanePosition": {
                        "longitudinalLanePositionValue": int(obj.matchedPosition.longitudinalLanePositionValue),
                        "longitudinalLanePositionConfidence": int(obj.matchedPosition.longitudinalLanePositionConfidenceValue),
                    }
                }
            return encoded_obj

        return {
            "cpm":{
             "header": {
                "protocolVersion":1,
                "messageID": 14,
                "stationID": 2
            },
            "cpm": {
                "generationDeltaTime": self.generationDeltaTime,
                "cpmParameters": {
                    "numberOfPerceivedObjects": len(self.cpmParameters.cpmPerceivedObjectContainer),
                    "perceivedObjectContainer": [encode_cpm_perceived_object(obj) for obj in self.cpmParameters.cpmPerceivedObjectContainer],
                    "managementContainer": {
                        "stationType": self.cpmParameters.managementContainer.stationType,
                        "referencePosition": encode_reference_position(self.cpmParameters.managementContainer.referencePosition),
                    }
                }
            }
        }
    }