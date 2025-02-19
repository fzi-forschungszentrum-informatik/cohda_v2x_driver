# -- BEGIN LICENSE BLOCK ----------------------------------------------
# -- END LICENSE BLOCK ------------------------------------------------
#
# ---------------------------------------------------------------------
# !\file
#
# \author  Albert Schotschneider <schotschneider@fzi.de>
# \date    2024-07-03
#
#
# ---------------------------------------------------------------------
from dataclasses import dataclass
from typing import Dict

from .its_pdu_header import ItsPduHeader


@dataclass
class SPATEM:
    header: ItsPduHeader

    @classmethod
    def from_dict(cls, data: Dict) -> "SPATEM":
        return cls(
            header=ItsPduHeader.from_dict(data.get("header")),
        )
