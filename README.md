# Cohda Driver

##
The driver was used in ITTRANS 2024 Karlsruhe. The Compatability of the driver has been tested with COHDA MK6 Devices.
An example configuration file for RSU can be found under `examples/conf` folder.
Special thanks to COHDA for permitting the publication of this driver.

For Python dependencies, we use the following packages:

| Package            | Version | Description                           |
| ------------------ | ------- | ------------------------------------- |
| asn1tools          | 0.166.0 | Parse ASN.1 files.                    |
| colorlog           | 6.8.2   | Colored output for logger.            |
| dataclasses-struct | 0.8.1   | C-structs for dataclass-like classes. |


Install all Python dependencies and the package itself with the following command:

```shell
pip install -r requirements.txt
pip install -e .
```


## Usage

You can run the example script under the `examples` folder.

```shell
python examples/cam_handler_mk6.py
python examples/cpm_handler_mk6.py
python examples/mapem_handler_mk6.py
```

| ETSI Message       | Version                  |
| ------------------ | ------------------------ |
| CAM                | EN 302 637-2             | 
| CPM                | ETSI TS 103 324 V0.0.22  | 
| MAPEM              | TS 103 301               |
| SPATEM             | TS 103 301               |



## Contributing

See the [Contributing Guide](CONTRIBUTING.md).


## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for details.



