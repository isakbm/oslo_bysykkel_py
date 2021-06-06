# oslo_bysykkel.py

This is just a cute little wrapper around the **gbfs** endpoint:

[https://gbfs.urbansharing.com/oslobysykkel.no/gbfs.json](https://gbfs.urbansharing.com/oslobysykkel.no/gbfs.json)

It uses the standard **json** and **requests** python packages.

## Create a python environment using conda

```shell
$ conda create -n oorigo python=3.9
$ conda activate oorigo
```

## Install directly from git (kinda cool)

```shell
$ (oorigo) pip install git+git://github.com/isakbm/oslo_bysykkel_py.git
```

## Test the package

Create *main.py* and fill it with the following contents

```python
import json
from oslo_bysykkel import API

api = API(client_identifier='OSLO-ORIGO-APPLICANT-CODE-CHALLENGE')
summary = api.get_summary_dict()

print(json.dumps(summary, indent='    '))
```

Then execute
```shell
$ python main.py
```

You should see some nice json output.
