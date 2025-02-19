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


@ds.dataclass(endian=ds.BIG_ENDIAN)
class CommonHeader:
    # Current version: 4
    protocol_version: ds.U8 = 4

    # 0 = BTP Data Request, 1 = BTP Data Indication
    message_id: ds.U8 = 0

    # Length of the BtpDataRequest in bytes.
    length: ds.U16 = 0


COMMON_HEADER_SIZE = ds.get_struct_size(CommonHeader)
