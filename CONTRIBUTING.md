# Welcome

This document is the contribution guide for the Cohda Driver.

## Adding a new ETSI message

Put the new ASN.1 files into a separate folder under the [`asn1`](asn1/) folder. Add the new
foldername to the `ETSI_MESSAGES` list in the `driver.py` file within the `CohdaDriver` class, i.e.:

```python
...
    ETSI_MESSAGES = ["cam", "cpm_tr103562", "mapem", "spatem", "new_etsi_msg"]
...
```

Add a new ETSI message class to the `cohda_driver.etsi_messages` module by creating a new Python
file. In the file, create a new `dataclass` and add the fields specified in the ETSI standard. Make
sure to create new dataclasses for non-atomic types/fields.

For every class, provide a `from_dict` method that returns an instance of the class. Make sure to
clamp values to the correct range and stick to the types specified in the ETSI standard.

Here is a minimal example:

```python
from dataclasses import dataclass
from typing import Dict


@dataclass
class NewEtsiMessage:
    field_1: int
    field_2: int

    @classmethod
    def from_dict(cls, data: Dict) -> "NewEtsiMessage":
        return cls(
            field_1=data.get("field_1"),
            field_2=data.get("field_2"),
        )
```

Afterwards, add the class to the `EtsiMessageClasses` type alias in the `driver.py` file.

```python
...
EtsiMessageClasses: TypeAlias = Union[CAM, SPATEM, NewEtsiMessage]
...
```


