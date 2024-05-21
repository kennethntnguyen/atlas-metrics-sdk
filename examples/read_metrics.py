import orjson, os, sys
from pydantic import BaseModel
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from atlas import MetricsReader, Filter, DeviceMetric, DeviceKind, CompressorMetric

"""
This example retrieves the suction pressure metrics for all compressors in the
Oxnard facility over the past 10 minutes and prints the average values for each
minute.
"""
json_output = "--json" in sys.argv
debug ="--debug" in sys.argv

device_kind = DeviceKind.compressor
metric_name = CompressorMetric.suction_pressure
facility_short_name = "oxnard"

metric = DeviceMetric(device_kind=device_kind, name=metric_name)
filter = Filter(facilities=[facility_short_name], metrics=[metric])
values = MetricsReader(debug=debug).read(filter)

if json_output:
    print(orjson.dumps(values, default=lambda x: x.model_dump() if isinstance(x, BaseModel) else x).decode("utf-8"))
    sys.exit(0)

for facility, metrics_values in values.items():
    print(facility)
    for metric_values in metrics_values:
        print(f"{metric_values.device_alias} \"{metric_values.device_name}\"")
        for value in metric_values.values:
            print(f"  {value.timestamp}: {value.value}")