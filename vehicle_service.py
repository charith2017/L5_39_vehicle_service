import hashlib
import json
import shutil
from datetime import date

SERVICE_RATES = {
    "Oil Change": 1500,
    "Wheel Alignment": 800,
    "General": 2500,
    "Brake Check": 1200,
}
SERVICE_RECORDS = {}


def add_service(vehicle_no, service_type="General", history=None):
    if not isinstance(vehicle_no, str) or not vehicle_no.strip():
        raise ValueError("Vehicle number must be a non-empty string")
    if not isinstance(service_type, str) or service_type not in SERVICE_RATES:
        raise ValueError("Unknown service type")
    if history is None:
        history = []
    entry = {
        "type": service_type,
        "cost": SERVICE_RATES[service_type],
        "date": str(date.today()),
    }
    SERVICE_RECORDS.setdefault(vehicle_no, []).append(entry)
    history.append(vehicle_no)
    return history


def cancel_service(vehicle_no, service_type):
    try:
        jobs = SERVICE_RECORDS[vehicle_no]
    except KeyError:
        print("No records for", vehicle_no)
        return False
    remaining = [job for job in jobs if job["type"] != service_type]
    SERVICE_RECORDS[vehicle_no] = remaining
    return len(remaining) < len(jobs)


def get_total_cost(vehicle_no):
    return sum(job["cost"] for job in SERVICE_RECORDS.get(vehicle_no, []))


def job_card_id(vehicle_no):
    return hashlib.sha256(vehicle_no.encode("utf-8")).hexdigest()[:8]


def busiest_vehicle():
    return max(SERVICE_RECORDS, key=lambda key: len(SERVICE_RECORDS[key]),
               default=None)


def save_records(file_name="services.json"):
    with open(file_name, "w", encoding="utf-8") as records_file:
        json.dump(SERVICE_RECORDS, records_file, indent=2)


def load_records(file_name="services.json"):
    with open(file_name, encoding="utf-8") as records_file:
        return json.load(records_file)


def backup_records(folder):
    return shutil.copy2("services.json", folder)


def main():
    add_service("KA01AB1234", "Oil Change")
    add_service("KA01AB1234", "Wheel Alignment")
    add_service("KA05XY9876")
    add_service("KA03MN4455", "Brake Check")
    cancel_service("KA05XY9876", "Brake Check")
    cancel_service("KA09ZZ0001", "General")
    cancel_service("KA03MN4455", "Brake Check")
    print("Total for KA01AB1234:", get_total_cost("KA01AB1234"))
    print("Total for KA05XY9876:", get_total_cost("KA05XY9876"))
    print("Job card for KA01AB1234:", job_card_id("KA01AB1234"))
    save_records()
    loaded = load_records()
    print("Vehicles on file:", len(loaded),
          "| busiest vehicle:", busiest_vehicle())


if __name__ == "__main__":
    main()
