# argo-probe-json

The package contains `check_json` probe which fetches JSON response and optionally parses it. If invoked with only URL, it will check only that the response is json and that status code is OK. The parsing of the response can be to check if the value of a wanted key is equal to expected value, or if value is numerical, it can check if it falls within defined warning and critical ranges, in which case the probe will return the corresponding status code. 

## Synopsis

### Required arguments

The probe has two required arguments:

* `-u`, `--url` which is the URL for which we are checking the JSON response, and
* `-t`, `--timeout` which is the time in seconds after which the connection will time out and probe will stop execution. If not defined, this value is by default 30.

### Optional arguments

In case the probe uses only mandatory arguments, it will simply check that the response is JSON and that the returned status code is OK. There are some optional arguments, however, that cause the probe to do more extensive checks. The arguments are as follows:

* `-k`, `--key` which is the key in JSON for which we wish to inspect the value;
* `-v`, `--target-value`  which is the target value to which the value of the key must be equal;
* `-w`, `--warning` which is the warning range - if the inspected value is in the requested range, the probe will return WARNING status;
* `-c`, `--critical` which is the critical range - if the inspected value is in the requested range, the probe will return CRITICAL status.

#### Nested keys

The probe is capable of inspecting the nested keys. For example, let us assume the JSON response is as follows:

```json
{
  "key1": {
    "key3": {
      "key4": "value4",
      "key5": "value5"
    },
    "key2": "value2"
  }
}
```

If we would like to inspect the value corresponding to nested key `key4` in the example above, we would define the `--key` argument for the probe with dots, as:

```
key1.key3.key4
```

#### Ranges definitions

Both warning and critical ranges are defined as strings, in format given in the table below.

| Range definition | The probe returns                             |
| --- |------------------------------------------------------------|
| 10 | Probe raises alert when value is inside [0, 10] range       |
|10: | Probe raises alert when value is inside [10, &infin;] range |
|10:20| Probe raises alert when value is inside [10, 20] range     |

## Examples

The probe can be used to simply inspect that the response is in JSON format and its status code is OK. For that, it is simply called with the mandatory arguments:

```
# /usr/libexec/argo/probes/json/check_json -u https://test.example.com/test.json -t 30
OK - JSON response OK
```

We can also inspect that the key's value is equal to the defined target value:

```
# /usr/libexec/argo/probes/json/check_json -u https://test.example.com/test.json -t 30 -k key1.key3.key4 --target-value value4
OK - key1.key3.key4 value is value4
```

Instead of checking if key's value corresponds to the target value, we can also inspect if value falls within warning and/or critical ranges (if value is numerical). For the sake of example, let us assume that the value is 20.

```
# /usr/libexec/argo/probes/json/check_json -u https://test.example.com/test.json -t 30 -k key1.key3.key4 -w 30 -c 15
WARNING - Value 20 in range 0:30
```

In case the value is in the defined critical range, the probe would return CRITICAL status:

```
# /usr/libexec/argo/probes/json/check_json -u https://test.example.com/test.json -t 30 -k key1.key3.key4 -w 50 -c 30
CRITICAL - Value 20 in range 0:30
```

Keep in mind that you cannot use `--target-value` argument with any of the ranges:

```
# /usr/libexec/argo/probes/json/check_json -u https://test.example.com/test.json -t 30 -k key1.key3.key4 --target-value value4 -w 30
usage: 
  Probe that checks JSON response given the URL
  -u URL -t TIMEOUT [-k KEY] [[-v TARGET_VALUE] | [-w WARNING] [-c CRITICAL]] 
  [-h]
check_json: error: You cannot use '--target-value' with the ranges
```
