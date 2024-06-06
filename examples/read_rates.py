import os
import sys
import orjson
from datetime import datetime
from pydantic import BaseModel
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import List
from atlas import AtlasClient, HourlyRates

def read_rates(facility_short_name: str, debug: bool = False) -> HourlyRates:
    """
    Return the past 24 hours of rates for the given facility.
    """
    client = AtlasClient(debug)
    try:
        facilities = client.list_facilities()
    except Exception as e:
        print(f"Error listing facilities: {e}")
        return {}

    facility = next((f for f in facilities if f.short_name == facility_short_name), None)
    if facility is None:
        print(f"Facility {facility_short_name} not found")
        return {}

    return client.get_hourly_rates(facility.organization_id, facility.agents[0].agent_id)

def print_rates(title: str, rates: List[HourlyRates]):
    if rates:
        print(title)
        for rate in rates:
            print(f"  {datetime.fromtimestamp(rate.start).strftime('%Y-%m-%d %H:%M:%S')}: {rate.rate}")

if __name__ == "__main__":
    json_output = "--json" in sys.argv
    debug ="--debug" in sys.argv
    facility = sys.argv[1] if len(sys.argv) > 1 else None
    if facility is None:
        print("Usage: python read_rates.py <facility>")
        sys.exit(1)

    rates = read_rates(facility)

    if json_output:
        print(orjson.dumps(rates, default=lambda x: x.model_dump() if isinstance(x, BaseModel) else x).decode("utf-8"))
        sys.exit(0)

    print(f"Rates for {facility.capitalize()}")
    print_rates("Usage Rate", rates.usage_rate)
    print_rates("Maximum Demand Charge", rates.maximum_demand_charge)
    print_rates("Time of Use Demand Charge", rates.time_of_use_demand_charge)
    print_rates("Day Ahead Market Rate", rates.day_ahead_market_rate)
    print_rates("Real Time Market Rate", rates.real_time_market_rate)
