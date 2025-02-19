# -- BEGIN LICENSE BLOCK ----------------------------------------------
# -- END LICENSE BLOCK ------------------------------------------------
#
# ---------------------------------------------------------------------
# !\file
#
# \author  Albert Schotschneider <schotschneider@fzi.de>
# \author  Melih Yazgan <yazgan@fzi.de>
# \date    2024-07-03
#
#
# ---------------------------------------------------------------------
from dataclasses import dataclass
from typing import Dict, List

from .its_pdu_header import ItsPduHeader


def clamp(value: float, min_value: float, max_value: float) -> float:
    return min(max_value, max(min_value, value))


@dataclass
class Altitude:
    altitude_value: int
    altitude_confidence: int

    @classmethod
    def from_dict(cls, data: Dict) -> "Altitude":
        return cls(
            altitude_value=clamp(data.get("altitudeValue", 0), -100000, 800001),
            altitude_confidence=clamp(data.get("altitudeConfidence", 0), 0, 15),
        )

    def to_dict(self) -> Dict:
        return {
            "altitudeValue": clamp(self.altitude_value, -100000, 800001),
            "altitudeConfidence": clamp(self.altitude_confidence, 0, 15),
        }


@dataclass
class Heading:
    heading_value: int
    heading_confidence: int

    @classmethod
    def from_dict(cls, data: Dict) -> "Heading":
        return cls(
            heading_value=clamp(data.get("headingValue", 0), 0, 3601),
            heading_confidence=clamp(data.get("headingConfidence", 0), 0, 127),
        )

    def to_dict(self) -> Dict:
        return {
            "headingValue": clamp(self.heading_value, 0, 3601),
            "headingConfidence": clamp(self.heading_confidence, 0, 127),
        }


@dataclass
class Speed:
    speed_value: int
    speed_confidence: int

    @classmethod
    def from_dict(cls, data: Dict) -> "Speed":
        return cls(
            speed_value=clamp(data.get("speedValue", 0), 0, 16382),
            speed_confidence=clamp(data.get("speedConfidence", 0), 0, 127),
        )

    def to_dict(self) -> Dict:
        return {
            "speedValue": clamp(self.speed_value, 0, 16382),
            "speedConfidence": clamp(self.speed_confidence, 0, 127),
        }


@dataclass
class VehicleLength:
    vehicle_length_value: int
    vehicle_length_confidence_indication: int

    @classmethod
    def from_dict(cls, data: Dict) -> "VehicleLength":
        return cls(
            vehicle_length_value=clamp(data.get("vehicleLengthValue", 1), 1, 1023),
            vehicle_length_confidence_indication=clamp(
                data.get("vehicleLengthConfidenceIndication", 0), 0, 4
            ),
        )

    def to_dict(self) -> Dict:
        return {
            "vehicleLengthValue": clamp(self.vehicle_length_value, 1, 1023),
            "vehicleLengthConfidenceIndication": clamp(
                self.vehicle_length_confidence_indication, 0, 4
            ),
        }


@dataclass
class LongitudinalAcceleration:
    longitudinal_acceleration_value: int
    longitudinal_acceleration_confidence: int

    @classmethod
    def from_dict(cls, data: Dict) -> "LongitudinalAcceleration":
        return cls(
            longitudinal_acceleration_value=clamp(
                data.get("longitudinalAccelerationValue", 0), -160, 160
            ),
            longitudinal_acceleration_confidence=clamp(
                data.get("longitudinalAccelerationConfidence", 0), 0, 102
            ),
        )

    def to_dict(self) -> Dict:
        return {
            "longitudinalAccelerationValue": clamp(self.longitudinal_acceleration_value, -160, 160),
            "longitudinalAccelerationConfidence": clamp(
                self.longitudinal_acceleration_confidence, 0, 102
            ),
        }


@dataclass
class Curvature:
    curvature_value: int
    curvature_confidence: int

    @classmethod
    def from_dict(cls, data: Dict) -> "Curvature":
        return cls(
            curvature_value=clamp(data.get("curvatureValue", 0), -1023, 1023),
            curvature_confidence=clamp(data.get("curvatureConfidence", 0), 0, 7),
        )

    def to_dict(self) -> Dict:
        return {
            "curvatureValue": clamp(self.curvature_value, -1023, 1023),
            "curvatureConfidence": clamp(self.curvature_confidence, 0, 7),
        }


@dataclass
class YawRate:
    yaw_rate_value: int
    yaw_rate_confidence: int

    @classmethod
    def from_dict(cls, data: Dict) -> "YawRate":
        return cls(
            yaw_rate_value=clamp(data.get("yawRateValue", 0), -32766, 32767),
            yaw_rate_confidence=clamp(data.get("yawRateConfidence", 0), 0, 8),
        )

    def to_dict(self) -> Dict:
        return {
            "yawRateValue": clamp(self.yaw_rate_value, -32766, 32767),
            "yawRateConfidence": clamp(self.yaw_rate_confidence, 0, 8),
        }


@dataclass
class PosConfidenceEllipse:
    semi_major_confidence: int
    semi_minor_confidence: int
    semi_major_orientation: int

    @classmethod
    def from_dict(cls, data: Dict) -> "PosConfidenceEllipse":
        return cls(
            semi_major_confidence=clamp(data.get("semiMajorConfidence", 0), 0, 4095),
            semi_minor_confidence=clamp(data.get("semiMinorConfidence", 0), 0, 4095),
            semi_major_orientation=clamp(data.get("semiMajorOrientation", 0), 0, 3601),
        )

    def to_dict(self) -> Dict:
        return {
            "semiMajorConfidence": clamp(self.semi_major_confidence, 0, 4095),
            "semiMinorConfidence": clamp(self.semi_minor_confidence, 0, 4095),
            "semiMajorOrientation": clamp(self.semi_major_orientation, 0, 3601),
        }


@dataclass
class ReferencePosition:
    latitude: int
    longitude: int
    position_confidence_ellipse: PosConfidenceEllipse
    altitude: Altitude

    @classmethod
    def from_dict(cls, data: Dict) -> "ReferencePosition":
        return cls(
            latitude=clamp(data.get("latitude", 0), -900000000, 900000001),
            longitude=clamp(data.get("longitude", 0), -1800000000, 1800000001),
            position_confidence_ellipse=PosConfidenceEllipse.from_dict(
                data.get("positionConfidenceEllipse", {})
            ),
            altitude=Altitude.from_dict(data.get("altitude", {})),
        )

    def to_dict(self) -> Dict:
        return {
            "latitude": clamp(self.latitude, -900000000, 900000001),
            "longitude": clamp(self.longitude, -1800000000, 1800000001),
            "positionConfidenceEllipse": self.position_confidence_ellipse.to_dict(),
            "altitude": self.altitude.to_dict(),
        }


@dataclass
class BasicContainer:
    station_type: int
    reference_position: ReferencePosition

    @classmethod
    def from_dict(cls, data: Dict) -> "BasicContainer":
        return cls(
            station_type=clamp(data.get("stationType", 0), 0, 255),
            reference_position=ReferencePosition.from_dict(data.get("referencePosition", {})),
        )

    def to_dict(self) -> Dict:
        return {
            "stationType": clamp(self.station_type, 0, 255),
            "referencePosition": self.reference_position.to_dict(),
        }


@dataclass
class BasicVehicleContainerHighFrequency:
    heading: Heading
    speed: Speed
    drive_direction: int
    vehicle_length: VehicleLength
    vehicle_width: int
    longitudinal_acceleration: LongitudinalAcceleration
    curvature: Curvature
    curvature_calculation_mode: int
    yaw_rate: YawRate

    @classmethod
    def from_dict(cls, data: Dict) -> "BasicVehicleContainerHighFrequency":
        return cls(
            heading=Heading.from_dict(data.get("heading", {})),
            speed=Speed.from_dict(data.get("speed", {})),
            drive_direction=clamp(data.get("driveDirection", 0), 0, 2),
            vehicle_length=VehicleLength.from_dict(data.get("vehicleLength", {})),
            vehicle_width=clamp(data.get("vehicleWidth", 0), 1, 62),
            longitudinal_acceleration=LongitudinalAcceleration.from_dict(
                data.get("longitudinalAcceleration", {})
            ),
            curvature=Curvature.from_dict(data.get("curvature", {})),
            curvature_calculation_mode=clamp(data.get("curvatureCalculationMode", 0), 0, 2),
            yaw_rate=YawRate.from_dict(data.get("yawRate", {})),
        )

    def to_dict(self) -> Dict:
        return {
            "heading": self.heading.to_dict(),
            "speed": self.speed.to_dict(),
            "driveDirection": clamp(self.drive_direction, 0, 2),
            "vehicleLength": self.vehicle_length.to_dict(),
            "vehicleWidth": clamp(self.vehicle_width, 1, 62),
            "longitudinalAcceleration": self.longitudinal_acceleration.to_dict(),
            "curvature": self.curvature.to_dict(),
            "curvatureCalculationMode": clamp(self.curvature_calculation_mode, 0, 2),
            "yawRate": self.yaw_rate.to_dict(),
        }


@dataclass
class ProtectedCommunicationZone:
    protected_zone_type: int
    expiry_time: int
    protected_zone_latitude: int
    protected_zone_longitude: int
    protected_zone_radius: int
    protected_zone_id: int

    @classmethod
    def from_dict(cls, _data: Dict) -> "ProtectedCommunicationZone":
        return cls(
            protected_zone_type=clamp(_data.get("protectedZoneType", 0), 0, 1),
            expiry_time=clamp(_data.get("expiryTime", 0), 0, 4398046511103),
            protected_zone_latitude=clamp(
                _data.get("protectedZoneLatitude", 0), -900000000, 900000001
            ),
            protected_zone_longitude=clamp(
                _data.get("protectedZoneLongitude", 0), -1800000000, 1800000001
            ),
            protected_zone_radius=clamp(_data.get("protectedZoneRadius", 0), 1, 255),
            protected_zone_id=clamp(_data.get("protectedZoneId", 0), 0, 134217727),
        )

    def to_dict(self) -> Dict:
        return {
            "protectedZoneType": clamp(self.protected_zone_type, 0, 1),
            "expiryTime": clamp(self.expiry_time, 0, 4398046511103),
            "protectedZoneLatitude": clamp(self.protected_zone_latitude, -900000000, 900000001),
            "protectedZoneLongitude": clamp(self.protected_zone_longitude, -1800000000, 1800000001),
            "protectedZoneRadius": clamp(self.protected_zone_radius, 1, 255),
            "protectedZoneId": clamp(self.protected_zone_id, 0, 134217727),
        }


@dataclass
class RSUContainerHighFrequency:
    protected_communication_zones_rsu: List[ProtectedCommunicationZone]

    @classmethod
    def from_dict(cls, data: Dict) -> "RSUContainerHighFrequency":
        return cls(
            protected_communication_zones_rsu=[
                ProtectedCommunicationZone.from_dict(zone)
                for zone in data.get("protectedCommunicationZonesRSU", [])
            ],
        )

    def to_dict(self) -> Dict:
        return {
            "protectedCommunicationZonesRSU": [
                zone.to_dict() for zone in self.protected_communication_zones_rsu
            ],
        }


@dataclass
class HighFrequencyContainer:
    basic_vehicle_container_high_frequency: BasicVehicleContainerHighFrequency
    rsu_container_high_frequency: RSUContainerHighFrequency

    @classmethod
    def from_dict(cls, data: Dict) -> "HighFrequencyContainer":
        return cls(
            basic_vehicle_container_high_frequency=BasicVehicleContainerHighFrequency.from_dict(
                data.get("basicVehicleContainerHighFrequency", {})
            ),
            rsu_container_high_frequency=RSUContainerHighFrequency.from_dict(
                data.get("rsuContainerHighFrequency", {})
            ),
        )

    def to_dict(self) -> Dict:
        return {
            "basicVehicleContainerHighFrequency": self.basic_vehicle_container_high_frequency.to_dict(),
            "rsuContainerHighFrequency": self.rsu_container_high_frequency.to_dict(),
        }


@dataclass
class CamParameters:
    basic_container: BasicContainer
    high_frequency_container: HighFrequencyContainer

    @classmethod
    def from_dict(cls, data: Dict) -> "CamParameters":
        return cls(
            basic_container=BasicContainer.from_dict(data.get("basicContainer", {})),
            high_frequency_container=HighFrequencyContainer.from_dict(
                data.get("highFrequencyContainer", {})
            ),
        )

    def to_dict(self) -> Dict:
        return {
            "basicContainer": self.basic_container.to_dict(),
            "highFrequencyContainer": self.high_frequency_container.to_dict(),
        }


@dataclass
class CoopAwareness:
    generation_delta_time: int
    cam_parameters: CamParameters

    @classmethod
    def from_dict(cls, data: Dict) -> "CoopAwareness":
        return cls(
            generation_delta_time=clamp(data.get("generationDeltaTime", 0), 0, 65535),
            cam_parameters=CamParameters.from_dict(data.get("camParameters", {})),
        )

    def to_dict(self) -> Dict:
        return {
            "generationDeltaTime": clamp(self.generation_delta_time, 0, 65535),
            "camParameters": self.cam_parameters.to_dict(),
        }


@dataclass
class CAM:
    header: ItsPduHeader
    cam: CoopAwareness

    @classmethod
    def from_dict(cls, data: Dict) -> "CAM":
        return cls(
            header=ItsPduHeader.from_dict(data.get("header")),
            cam=CoopAwareness.from_dict(data.get("cam")),
        )

    def to_dict(self) -> Dict:
        return {
            "header": self.header.to_dict(),
            "cam": self.cam.to_dict(),
        }
