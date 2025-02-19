#!/usr/bin/env python3
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
import time

from cohda_driver.etsi_messages.cam import CAM
from cohda_driver.etsi_message_type import EtsiMessageType
from cohda_driver.driver import CohdaDriver


def main() -> None:
    driver = CohdaDriver("localhost", "127.0.0.1", 5000, 5001)

    driver.setup_callback(callback=cam_callback, etsi_msg_type=EtsiMessageType.CAM)
    driver.start_loop()

    try:
        run()
    except KeyboardInterrupt:
        driver.stop_loop()


def run() -> None:
    while True:
        time.sleep(1)


def cam_callback(message: CAM) -> None:
    print(message)


if __name__ == "__main__":
    main()
