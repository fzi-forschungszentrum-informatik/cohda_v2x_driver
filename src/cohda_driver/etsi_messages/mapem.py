# -- BEGIN LICENSE BLOCK ----------------------------------------------
# -- END LICENSE BLOCK ------------------------------------------------
#
# ---------------------------------------------------------------------
# !\file
#
# \author  Melih Yazgan <yazgan@fzi.de>
# \date    2024-07-08
#
#
# ---------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import Dict, List

from .its_pdu_header import ItsPduHeader

@dataclass
class MAPEMNode:
	offset_x: float = 0
	offset_y: float = 0

@dataclass
class MAPEMNodeList:
	mapemNodeList: List[MAPEMNode] = field(default_factory=list)

@dataclass
class MAPEMGenericLane:
	laneId: int
	ingressApproach: int = 0
	egressApproach: int = 0
	laneAttributesType: int = 0
	connectionSinkLaneId: List[int] = field(default_factory=list)
	connectionGroup: List[int] = field(default_factory=list)
	mapemNodeList: MAPEMNodeList = field(default_factory=MAPEMNodeList)

@dataclass
class ReferencePosition:
	latitude: float
	longitude: float

@dataclass
class IntersectionGeometry:
	descriptiveName: str
	intersectionReferenceId: int
	intersectionReferenceIdRegion: int
	revision: int
	laneWidth: int
	refPoint: ReferencePosition
	genericLaneListSet: List[MAPEMGenericLane] = field(default_factory=list)

@dataclass
class MAPData:
	msgIssueRevision: int
	intersectionGeometryList: List[IntersectionGeometry] = field(default_factory=list)

@dataclass
class MAPEM:
	header: ItsPduHeader
	mapData: MAPData = field(default_factory=MAPData)

	@classmethod
	def from_dict(cls, data: Dict) -> "MAPEM":
		header = ItsPduHeader.from_dict(data.get("header"))

		map_data = MAPData(msgIssueRevision=data["map"]["msgIssueRevision"])
		for intersection in data["map"]["intersections"]:
			ref_position = ReferencePosition(
				latitude=intersection["refPoint"]["lat"]* 1e-7,
				longitude=intersection["refPoint"]["long"]* 1e-7,
			)
			intersection_geometry = IntersectionGeometry(
				descriptiveName=intersection["name"],
				intersectionReferenceId=intersection["id"]["id"],
				intersectionReferenceIdRegion=intersection["id"]["region"],
				revision=intersection["revision"],
				laneWidth=intersection["laneWidth"],
				refPoint=ref_position,
				genericLaneListSet=[]
			)

			for lane in intersection["laneSet"]:
				generic_lane = MAPEMGenericLane(
					laneId=lane["laneID"],
					ingressApproach=lane.get("ingressApproach", 0),
					egressApproach=lane.get("egressApproach", 0),
					laneAttributesType=lane["laneAttributes"]["laneType"][0]
				)

				connectionSinkLaneId = [connect_id["connectingLane"]["lane"] for connect_id in lane.get("connectsTo", [])]
				connectionGroup = [connect_id["signalGroup"] for connect_id in lane.get("connectsTo", []) if "signalGroup" in connect_id]
				generic_lane.connectionSinkLaneId = connectionSinkLaneId
				generic_lane.connectionGroup = connectionGroup

				lane_node_list = MAPEMNodeList()
				for node in lane["nodeList"][1]:
					lane_node = MAPEMNode(
						offset_x=node["delta"][1]["x"]/100,
						offset_y=node["delta"][1]["y"]/100,
					)
					lane_node_list.mapemNodeList.append(lane_node)

				generic_lane.mapemNodeList = lane_node_list
				intersection_geometry.genericLaneListSet.append(generic_lane)

			map_data.intersectionGeometryList.append(intersection_geometry)

		return cls(header=header, mapData=map_data)
