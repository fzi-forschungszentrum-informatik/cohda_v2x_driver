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
from typing import Dict


@dataclass
class ItsPduHeader:
    protocol_version: int
    message_id: int
    station_id: int

    @classmethod
    def from_dict(cls, data: Dict) -> "ItsPduHeader":
        return cls(
            protocol_version=data["protocolVersion"],
            message_id=data.get("messageID") or data.get("messageId") or 0,
            station_id=data.get("stationID") or data.get("stationId") or 0,
        )

    def to_dict(self) -> Dict:
        return {
            "protocolVersion": self.protocol_version,
            "messageID": self.message_id,
            "stationID": self.station_id,
        }
