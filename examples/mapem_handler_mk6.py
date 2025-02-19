#!/usr/bin/env python3
# -- BEGIN LICENSE BLOCK ----------------------------------------------
# -- END LICENSE BLOCK ------------------------------------------------
#
# ---------------------------------------------------------------------
# !\file
#
# \author  Melih Yazgan <yazgan@fzi.de>
# \date    2024-07-05
#
#
# ---------------------------------------------------------------------
import time

from cohda_driver.etsi_messages.mapem import MAPEM

from cohda_driver.etsi_message_type import EtsiMessageType

from cohda_driver.driver import CohdaDriver

def main() -> None:
    driver = CohdaDriver("141.21.47.177", "141.21.45.111", 4400, 4401)

    driver.setup_callback(callback=mapem_callback, etsi_msg_type=EtsiMessageType.MAPEM)

    driver.start_loop()
    try:
        run()
    except KeyboardInterrupt:
        driver.stop_loop()

def run() -> None:
    while True:
        time.sleep(1)

def mapem_callback(message: MAPEM) -> None:
    print(message)

if __name__ == "__main__":
    main()