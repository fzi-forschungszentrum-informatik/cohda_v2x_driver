# -- BEGIN LICENSE BLOCK ----------------------------------------------
# -- END LICENSE BLOCK ------------------------------------------------
#
# ---------------------------------------------------------------------
# !\file
#
# \author  Albert Schotschneider <schotschneider@fzi.de>
# \author  Melih Yazgan <yazgan@fzi.de>
# \date    2024-07-09
#
#
# ---------------------------------------------------------------------

# -------- System imports -------------
import socket
import threading

from typing import Union, List, Dict, Callable
from pathlib import Path

# -------- Third party imports -------------
import asn1tools

from typing_extensions import TypeAlias

# -------- Local imports -------------
from cohda_driver import btp_request
from cohda_driver.common_header import COMMON_HEADER_SIZE
from cohda_driver.btp_indication import BTP_DATA_INDICATION_SIZE

from cohda_driver.etsi_messages import CAM
from cohda_driver.etsi_messages import SPATEM
from cohda_driver.etsi_messages import CPM
from cohda_driver.etsi_messages import MAPEM
from cohda_driver.etsi_messages import ItsPduHeader
from cohda_driver.etsi_message_type import EtsiMessageType

from cohda_driver.logger import logger

EtsiMessageClasses: TypeAlias = Union[CAM, SPATEM]


def get_asn_files_from_dir(path: Path) -> List[Path]:
    """
    Get ASN.1 files from a directory.

    Parameters
    ----------
    path : pathlib.Path
        Path to directory.

    Returns
    -------
    List[pathlib.Path]
        List of ASN.1 files.
    """
    return [f for f in path.iterdir() if f.is_file()]


class CohdaDriver:
    """
    Cohda Driver class for interfacing with a Cohda device.

    Class Attributes
    ---------------
    BUFFER_SIZE : int
        Size of the buffer for receiving data.
    HEADER_SIZE : int
        Size of the full header for an incoming UDP packet.
    ASN_DIR : pathlib.Path
        Path to the directory containing the ASN.1 specifications.
    ETSI_MESSAGES : List[str]
        List of ETSI messages to be loaded for the ASN.1
        specifications. These should match the folder names in the
        ASN.1 directory.
    """

    BUFFER_SIZE = 4096
    HEADER_SIZE = COMMON_HEADER_SIZE + BTP_DATA_INDICATION_SIZE

    ASN_DIR = Path(__file__).parent.parent.parent / "asn1"
    ETSI_MESSAGES = ["cam", "cpm_tr103562", "mapem", "spatem"]

    def __init__(self, host_ip: str, cohda_ip: str, cohda_ind_port: int, cohda_req_port: int):
        """
        Initialize the Cohda Driver class.

        Parameters
        ----------
        host_ip : str
            Host IP address of the machine running this driver and connected to the Cohda device.
        cohda_ip : str
            Cohda device IP address.
        cohda_ind_port : int
            Cohda Indication Port for receiving data.
        cohda_req_port : int
            Cohda Request Port for sending data.
        """
        self._cohda_ip = cohda_ip
        self._cohda_req_port = cohda_req_port
        self._callbacks = {}
        self._is_running = False
        self._run_thread = threading.Thread(target=self._run, daemon=True)

        # -----------------------------
        # ASN.1 Specification Setup
        # -----------------------------
        logger.info(f"Loading ASN.1 specifications from {self.ASN_DIR} ...")
        self._specs: Dict[str, asn1tools.compiler.Specification] = {}
        for etsi_message in self.ETSI_MESSAGES:
            logger.debug(f"Adding '{etsi_message}' specification.")
            self._specs[etsi_message] = asn1tools.compile_files(
                get_asn_files_from_dir(self.ASN_DIR / etsi_message),
                codec="uper",
                numeric_enums=True,
            )

        # -----------------------------
        # Socket Setup
        # -----------------------------
        logger.info(f"Binding to {host_ip}:{cohda_ind_port} for receiving packets.")
        logger.info(f"Packets will be sent to {cohda_ip}:{cohda_req_port}.")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(5)
        self.sock.bind((host_ip, cohda_ind_port))

        logger.info("Driver initialized.")

    def setup_callback(
        self,
        callback: Callable[[EtsiMessageClasses], None],
        etsi_msg_type: EtsiMessageType,
    ):
        """
        Add callback for the given etsi_msg_type.

        Parameters
        ----------
        callback : Callable[[EtsiMessageClasses], None]
            Callback function that will be called when the
            etsi_msg_type is received. The function must have the
            following signature:

            ```
            callback(etsi_msg: EtsiMessageClasses)
            ```

            where EtsiMessageClasses is a union of all ETSI messages.

        etsi_msg_type : EtsiMessageType
            ETSI message type for which the callback should be added.
        """
        if etsi_msg_type in self._callbacks:
            logger.warning(f"Callback for {etsi_msg_type} already exists. Will replace it.")
        logger.info(f"Adding callback for '{etsi_msg_type}'.")
        self._callbacks[etsi_msg_type] = callback

    def start_loop(self):
        """
        Start the driver loop.
        """
        logger.info("Starting driver loop.")
        self._is_running = True
        self._run_thread.start()

    def stop_loop(self):
        """
        Stop the driver loop.
        """
        logger.info("Stopping driver loop.")
        self._is_running = False
        self._run_thread.join()

    def _run(self):
        """
        Run the driver and receive and process incoming packets.
        """
        if not self._callbacks:
            logger.warning("No callbacks added. Will not receive any packets.")
            self._is_running = False
            return

        while self._is_running:
            try:
                data, _ = self.sock.recvfrom(self.BUFFER_SIZE)
            except socket.timeout:
                logger.warning("Trying to receive data...")
                continue
            data = data[self.HEADER_SIZE :]

            its_pdu_header = ItsPduHeader.from_dict(self._specs["cam"].decode("ItsPduHeader", data))
            protocol_version = its_pdu_header.protocol_version
            message_type = EtsiMessageType(its_pdu_header.message_id)
            if protocol_version not in [1, 2]:
                logger.warning(f"Unsupported protocol version: {protocol_version}")
                continue

            if message_type == EtsiMessageType.CAM and protocol_version == 2:
                try:
                    cam_msg = CAM.from_dict(self._specs["cam"].decode("CAM", data))
                    self._callbacks[EtsiMessageType.CAM](cam_msg)
                except Exception as e:
                    logger.warning(f"Error decoding CAM message: {e}")
                    continue
            elif message_type == EtsiMessageType.SPATEM and protocol_version == 2:
                spatem_msg = SPATEM.from_dict(self._specs["spatem"].decode("SPATEM", data))
                self._callbacks[EtsiMessageType.SPATEM](spatem_msg)
            elif message_type == EtsiMessageType.CPM and protocol_version == 2:
                cpm_msg = CPM.from_dict(self._specs["cpm_tr103562"].decode("CPM", data))
                self._callbacks[EtsiMessageType.CPM](cpm_msg)
            elif message_type == EtsiMessageType.MAPEM and protocol_version == 2:
                mapem_msg = MAPEM.from_dict(self._specs["mapem"].decode("MAPEM", data))
                self._callbacks[EtsiMessageType.MAPEM](mapem_msg)
            else:
                logger.warning(f"Unsupported message type: {message_type}")

    def send_request(self, message_type: EtsiMessageType, message_data: dict):
        """
        Send a request to the Cohda device using btp_request.

        Parameters
        ----------
        message_type : EtsiMessageType
            The type of ETSI message to send.
        message_data : dict
            The data of the message to send, in a dictionary format.
        """

        # Serialize the message data using the ASN.1 specification
        try:
            serialized_data = self._specs[str(message_type)].encode("CPM", message_data["cpm"])
            btp_packet = btp_request.create_btp_request_packet(EtsiMessageType.CPM, serialized_data)
            self.sock.sendto(btp_packet, (self._cohda_ip, self._cohda_req_port))
        except Exception as e:
            logger.error(f"Failed to serialize message data for {message_type}: {e}")
