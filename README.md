# Atlas Metrics SDK

## Overview

The Atlas Metrics SDK is a Python library that provides a simple interface for
retrieving metrics from the Atlas platform.  The library provides both
high-level and low-level APIs, allowing users to choose the appropriate level of
abstraction based on their needs. The high-level API simplifies usage, while the
low-level API offers more flexibility and control.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/crossnokaye/atlas-metrics-sdk.git
    cd atlas-metrics-sdk
    ```

2. Create a virtual environment and install the dependencies:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

## Configuration

Create a configuration file at `~/.config/atlas/config.toml` with the following
content:

```toml
[production]
refresh_token = "your_refresh_token_here"
```

## Get Started

The `examples` directory contains sample code that demonstrates how to use the
library. To run the examples, execute the following command:

```bash
python examples/read_metrics.py
```

The examples are:

- `read_metrics.py`: Demonstrates how to retrieve metric values using the high-level API.
- `list_facilities.py`: Demonstrates how to list facilities using the low-level API.
- `list_devices.py`: Demonstrates how to list devices for a facility using the low-level API.

Each example can print the output in plain text or JSON format. To print the output in JSON format, add the `--json` flag:

```bash
python examples/read_metrics.py --json
```

## High-Level API: MetricsReader

The `MetricsReader` class provides a simplified interface for retrieving metric point values.

### Example Usage

```python
from datetime import datetime
from atlas import MetricsReader, Filter, DeviceMetric, CompressorMetric, DeviceKind

# Define a filter
filter = Filter(
    facilities=['facility'],
    metrics=[DeviceMetric(
        device_kind=DeviceKind.compressor,
        name=CompressorMetric.suction_pressure,
    )]
)

# Retrieve metric values
start_time = datetime(2023, 5, 1, 0, 0, 0)
end_time = datetime(2023, 5, 1, 23, 59, 59)
interval = 60  # 1 minute interval

data = MetricsReader().read(filter, start=start_time, end=end_time, interval=interval)
```

## Low-Level API: AtlasClient

The `AtlasClient` class provides a more flexible and lower-level interface for
interacting with the Atlas platform. This class allows for more complex
operations and greater control over the API interactions.

### Example Usage

```Python
from atlas import AtlasClient

# Initialize AtlasClient
client = AtlasClient()

# List facilities
facilities = client.list_facilities()
print(facilities)

# List devices for a facility
org_id = "organization_id"
agent_id = "agent_id"
devices = client.list_devices(org_id, agent_id)
print(devices)

# Get point IDs for device aliases
point_aliases = ["alias1", "alias2"]
point_ids = client.get_point_ids(org_id, agent_id, point_aliases)
print(point_ids)

# Get historical values
start_time = datetime(2023, 5, 1, 0, 0, 0)
end_time = datetime(2023, 5, 1, 23, 59, 59)
interval = 60  # 1 minute interval
historical_values = client.get_historical_values(org_id, agent_id, list(point_ids.values()), start=start_time, end=end_time, interval=interval)
print(historical_values)
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
