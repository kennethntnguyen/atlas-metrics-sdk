from enum import Enum
from pydantic import BaseModel
from typing import List, Dict, Union

class Agent(BaseModel):
    agent_id: str

class Facility(BaseModel):
    organization_id: str
    facility_id: str
    display_name: str
    short_name: str
    address: str
    timezone: str
    agents: List[Agent]

class PropertyValue(BaseModel):
    alias: str
    name: str
    kind: str
    bias: str

class Property(BaseModel):
    key: str
    value: PropertyValue

class Connection(BaseModel):
    id: str
    kind: str
    direction: str

class Device(BaseModel):
    id: str
    name: str
    alias: str
    kind: str
    properties: List[Property] = []

class AnalogValues(BaseModel):
    timestamps: List[int]
    values: List[float]

class DiscreteValues(BaseModel):
    timestamps: List[int]
    values: List[bool]

class PointValues(BaseModel):
    analog: AnalogValues = None
    discrete: DiscreteValues = None

class AggregateBy(str, Enum):
    avg = "avg"
    min = "min"
    max = "max"
    first = "first"
    last = "last"

class HistoricalValues(BaseModel):
    point_id: str
    values: Dict[AggregateBy, PointValues]

class DeviceKind(str, Enum):
    compressor = "compressor"
    evaporator = "evaporator"
    condenser = "condenser"
    vessel = "vessel"

class CompressorMetric(str, Enum):
    discharge_pressure = "DischargePressure"
    discharge_temperature = "DischargeTemperature"
    suction_pressure = "SuctionPressure"
    suction_temperature = "SuctionTemperature" 

class CondenserMetric(str, Enum):
    discharge_pressure = "DischargePressure"
    discharge_temperature = "DischargeTemperature"

class EvaporatorMetric(str, Enum):
    supply_temperature = "SupplyTemperature"
    return_temperature = "ReturnTemperature"

class VesselMetric(str, Enum):
    suction_pressure = "SuctionPressure"

DeviceMetricName = Union[CompressorMetric, CondenserMetric, EvaporatorMetric, VesselMetric]

class DeviceMetric(BaseModel):
    name: DeviceMetricName
    device_kind: DeviceKind

device_metric_mapping = {
    DeviceKind.compressor: CompressorMetric,
    DeviceKind.condenser: CondenserMetric,
    DeviceKind.evaporator: EvaporatorMetric,
    DeviceKind.vessel: VesselMetric
}

def is_valid_metric(metric: DeviceMetric) -> bool:
    """
    Check if the metric is valid for the given device kind.
    """
    return metric.name in device_metric_mapping[metric.device_kind]