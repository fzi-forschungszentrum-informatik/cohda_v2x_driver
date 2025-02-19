# -- BEGIN LICENSE BLOCK ----------------------------------------------
# -- END LICENSE BLOCK ------------------------------------------------
#
# ---------------------------------------------------------------------
# !\file
#
# \author  Albert Schotschneider <schotschneider@fzi.de>
# \date    2024-07-03
#
# This module implements the BTP Data Request Header.
# ---------------------------------------------------------------------
import dataclasses_struct as ds

from typing_extensions import Annotated

from .common_header import CommonHeader
from .etsi_message_type import EtsiMessageType


btp_ports = {
    EtsiMessageType.CAM: 2001,
    EtsiMessageType.DENM: 2002,
    EtsiMessageType.MAPEM: 2003,
    EtsiMessageType.SPATEM: 2004,
    EtsiMessageType.SAEM: 2005,
    EtsiMessageType.IVIM: 2006,
    EtsiMessageType.CPM: 2009,
}

# According to Cohda Documentation, the following are used for transport:
#   4 = GeoBroadCast (GBC), used for DENM, MAP, SPAT and IVI
#   7 = SingleHopBroadcast (SHB), used for CAM, SAEM
gn_packet_transports = {
    EtsiMessageType.CAM: 7,
    EtsiMessageType.DENM: 4,
    EtsiMessageType.MAPEM: 4,
    # This might be wrong, but setting it to 4 will lead to SPATEMs not being sent over the air.
    EtsiMessageType.SPATEM: 7,
    EtsiMessageType.IVIM: 4,
    EtsiMessageType.CPM: 7,
    EtsiMessageType.GENERIC: 7,
}

gn_traffic_classes = {
    EtsiMessageType.CAM: 0x02,
    EtsiMessageType.DENM: 0x01,
    EtsiMessageType.MAPEM: 0x03,
    EtsiMessageType.SPATEM: 0x03,
    EtsiMessageType.IVIM: 0x03,
    EtsiMessageType.CPM: 0x02,
    EtsiMessageType.GENERIC: 0x02,
}


@ds.dataclass(endian=ds.BIG_ENDIAN)
class BtpDataRequest:
    # 2 = BTP-B
    btp_type: ds.U8 = 2

    # 4 = GeoBroadCast (GBC), used for DENM, MAP, SPAT and IVI
    # 7 = SingleHopBroadcast (SHB), used for CAM, SAEM
    gn_packet_transport: ds.U8 = 0

    # CAM = 0x02 (DP3), DENM = 0x01, MAP, SPAT, IVIM, SAEM = 0x03
    gn_traffic_class: ds.U8 = 0

    # If set to 0, use ItsGnMaxPacketLifetime parameter from .conf file.
    gn_max_pkt_lifetime: ds.U8 = 0

    # 2001 = CAM, 2002 = DENM, 2003 = MAP, 2004 = SPAT, 2005 = SAEM, 2006 = IVIM
    btp_destination_port: ds.U16 = 0
    btp_destination_port_info: ds.U16 = 0

    # Latitude and longitude (only for GBC and GUC) in 1/10 microdegree
    gn_destination_lat: ds.I32 = 498664720
    gn_destination_lon: ds.I32 = 88604720
    gn_destination_distance_a: ds.U16 = 1
    gn_destination_distance_b: ds.U16 = 1
    gn_destination_angle: ds.U16 = 2
    gn_destination_shape: ds.U8 = 1
    reserved_0: ds.U8 = 0

    # 0x00 = Default, uses the configured profile in the .conf
    # 0x40 = C-V2X
    # 0x80 = G5
    gn_comms_profile: ds.U8 = 0x80
    gp_repeat_interval: ds.U8 = 0

    # 0 = Security disabled, the remaining security parameters are ignored
    # 1 = Security enabled, SSP bitmap type
    # 2 = Opaque type (e.g. used in the SAEM message)
    gn_security_profile: ds.U8 = 0
    gn_security_ssp_bits_length: ds.U8 = 0
    ssp: Annotated[bytes, 36] = bytes(36)

    # Payload length in bytes
    data_length: ds.U16 = 0


def create_btp_request_packet(message_type: EtsiMessageType, data: bytes) -> bytes:
    common_header = CommonHeader()
    common_header.length = BTP_REQUEST_SIZE + len(data)

    btp_header = BtpDataRequest()
    btp_header.gn_packet_transport = gn_packet_transports[message_type]
    btp_header.gn_traffic_class = gn_traffic_classes[message_type]
    btp_header.btp_destination_port = btp_ports[message_type]
    btp_header.data_length = 0xFFFF

    return common_header.pack() + btp_header.pack() + data


BTP_REQUEST_SIZE = ds.get_struct_size(BtpDataRequest)
