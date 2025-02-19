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
import dataclasses_struct as ds

from typing_extensions import Annotated


@ds.dataclass(endian=ds.BIG_ENDIAN)
class BtpDataIndication:
    btp_type: ds.U8 = 2
    gn_packet_transport: ds.U8 = 0
    gn_traffic_class: ds.U8 = 0
    gn_max_pkt_lifetime: ds.U8 = 0

    btp_destination_port: ds.U16 = 0
    btp_destination_port_info: ds.U16 = 0

    gn_destination_lat: ds.I32 = 498664720
    gn_destination_lon: ds.I32 = 88604720

    gn_destination_distance_a: ds.U16 = 1
    gn_destination_distance_b: ds.U16 = 1

    gn_destination_angle: ds.U16 = 2
    gn_destination_shape: ds.U8 = 1
    reserved_0: ds.U8 = 0

    gn_security_profile: ds.U8 = 0
    gn_security_parser_res: ds.U8 = 0
    gn_security_verify_res: ds.U8 = 0
    gn_sec_ssp_bits_length: ds.U8 = 0

    gn_security_its_aid: ds.U32 = 0

    gn_sec_ssp_bits: Annotated[bytes, 32] = bytes(32)
    gn_sec_cert_id: Annotated[bytes, 8] = bytes(8)
    data_length: ds.U16 = 0xFFFF


BTP_DATA_INDICATION_SIZE = ds.get_struct_size(BtpDataIndication)
