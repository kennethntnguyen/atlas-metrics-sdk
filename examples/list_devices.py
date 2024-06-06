import os
import sys
import orjson
from collections import defaultdict
from typing import Dict
from pydantic import BaseModel
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from atlas import AtlasClient

class PropertyValue(BaseModel):
    name: str
    kind: str
    bias: str
    alias: str

def list_devices(debug: bool = False) -> Dict[str, Dict[str, Dict[str, Dict[str, PropertyValue]]]]:
    """
    Return the device properties of all devices across all facilities indexed by
    facility name, then by device kind, then by device name, then by property
    name.

    example:
    {
        "Facility 1": {
            "Compressors": {
                "Comp 1": {
                    "SuctionPressure": {
                        "name": "Suction Pressure",
                        "kind": "analog",
                        "bias": "output",
                        "alias": "comp1_suction_pressure"
                    }
                }
            }
        }
    }
    """
    client = AtlasClient(debug)
    try:
        facilities = client.list_facilities()
    except Exception as e:
        print(f"Error listing facilities: {e}")
        return {}

    all_devices = {}
    for facility in sorted(facilities, key=lambda facility: facility.display_name):
        if not facility.agents:
            continue
        device_map = defaultdict(list)
        try:
            devices = client.list_devices(facility.organization_id, facility.agents[0].agent_id)
        except Exception as e:
            print(f"Error listing devices for facility {facility.display_name}: {e}")
            continue
        for device in sorted(devices, key=lambda device: device.name):
            device_map[device.kind].append(device)

        device_dict = {}
        for kind, devices in device_map.items():
            if len(devices) == 0:
                continue
            kind_dict = {}
            for device in sorted(devices, key=lambda device: device.name):
                properties_dict = {
                    prop.key: PropertyValue(name=prop.value.name, kind=prop.value.kind, bias=prop.value.bias, alias=prop.value.alias)
                    for prop in device.properties
                }
                if len(device.upstream) > 0:
                    properties_dict["upstream"] = {conn.kind: conn.device_id for conn in device.upstream}
                if len(device.downstream) > 0:
                    properties_dict["downstream"] = {conn.kind: conn.device_id for conn in device.downstream}
                if len(properties_dict) > 0:
                    kind_dict[device.name] = properties_dict
            if len(kind_dict) > 0:
                device_dict[kind.title() + "s"] = kind_dict

        all_devices[facility.display_name] = device_dict

    return all_devices

if __name__ == "__main__":
    json_output = "--json" in sys.argv
    debug ="--debug" in sys.argv

    devices = list_devices(debug)

    if json_output:
        print(orjson.dumps(devices, default=lambda x: x.model_dump() if isinstance(x, BaseModel) else x).decode("utf-8"))
        sys.exit(0)

    for facility_name, facility in devices.items():
        print(f"Facility: {facility_name}")
        for kind, devices in facility.items():
            print(f"  {kind}:")
            for device_name, properties in devices.items():
                print(f"    {device_name}")
                for _, prop in properties.items():
                    print(f"      {prop.name} ({prop.kind} {prop.bias}): {prop.alias}")
