#!/usr/bin/env python3
# -- BEGIN LICENSE BLOCK ----------------------------------------------
# -- END LICENSE BLOCK ------------------------------------------------
#
# ---------------------------------------------------------------------
# !\file
#
# \author  Melih Yazgan <yazgan@fzi.de>
# \date    2024-07-09
#
#
# ---------------------------------------------------------------------
import time

from cohda_driver.etsi_messages.cpm import CPM

from cohda_driver.etsi_message_type import EtsiMessageType

from cohda_driver.driver import CohdaDriver

def main() -> None:
	driver = CohdaDriver("141.21.47.177","141.21.45.111", 4400, 4401)

	driver.setup_callback(callback=cpm_callback, etsi_msg_type=EtsiMessageType.CPM)

	driver.start_loop()

	try:
		run(driver)
	except KeyboardInterrupt:
		driver.stop_loop()

def run(driver) -> None:
	default_cpm = CPM()  # Assuming CPM() initializes a default request
	while True:
		# NOTE: This is a dummy example.
		driver.send_request('cpm_tr103562', default_cpm.to_dict())
		time.sleep(1)
        
def cpm_callback(message: CPM) -> None:
	print(message)

if __name__ == "__main__":
	main()