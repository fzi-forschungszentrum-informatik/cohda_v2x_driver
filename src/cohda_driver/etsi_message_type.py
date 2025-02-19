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
from enum import Enum


class EtsiMessageType(Enum):
    UNKNOWN = 0
    DENM = 1
    CAM = 2
    POIM = 3
    SPATEM = 4
    MAPEM = 5
    IVIM = 6
    RFU1 = 7
    RFU2 = 8
    SREM = 9
    SSEM = 10
    EVCSN = 11
    SAEM = 12
    RTCMEM = 13
    CPM = 14
    IMZM = 15
    VAM = 16
    DSM = 17
    PCIM = 18
    PCVM = 19
    MCM = 20
    PAM = 21
    GENERIC = 98
    UNKNOWN_2 = 99
