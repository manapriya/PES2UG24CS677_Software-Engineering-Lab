"""Automated parking lot and slot manager.

Parks vehicles by licence plate, frees occupied slots, computes surge
rates and exports parking manifests.
"""
import hashlib
import json
import os
import secrets

PARKING_SLOTS = {
    "P01": {"plate": "KA01AB1234", "hours": 2, "rate": 20.0,
            "is_occupied": True},
    "P02": {"plate": "TN07CD5678", "hours": 0, "rate": 20.0,
            "is_occupied": False},
    "P03": {"plate": "MH02EF9012", "hours": 4, "rate": 30.0,
            "is_occupied": True},
}

STATS = {"total_collections": 0.0}


def park_vehicle(slot_id, plate_no, hours_booked=1, entry_logs=None):
    """Park a vehicle in a free slot; return True on success."""
    if slot_id not in PARKING_SLOTS or PARKING_SLOTS[slot_id]["is_occupied"]:
        return False
    if entry_logs is None:
        entry_logs = []
    slot = PARKING_SLOTS[slot_id]
    slot["plate"] = plate_no
    slot["hours"] = hours_booked
    slot["is_occupied"] = True
    STATS["total_collections"] += slot["rate"] * hours_booked
    entry_logs.append(
        f"Vehicle {plate_no} parked at slot {slot_id} for "
        f"{hours_booked} hours with total charge calculated"
    )
    return True


def release_slot(slot_id):
    """Free a slot; return False if the slot does not exist."""
    slot = PARKING_SLOTS.get(slot_id)
    if slot is None:
        return False
    slot["is_occupied"] = False
    slot["plate"] = ""
    slot["hours"] = 0
    return True


def check_slot_availability(slot_id):
    """Return True if the slot exists and is free."""
    slot = PARKING_SLOTS.get(slot_id)
    return slot is not None and not slot["is_occupied"]


def calculate_parking_fee(slot_id, surge_multiplier=1.0):
    """Return the hourly rate of a slot scaled by a surge multiplier."""
    if not isinstance(surge_multiplier, (int, float)) or surge_multiplier < 0:
        raise ValueError("surge_multiplier must be a non-negative number")
    return PARKING_SLOTS[slot_id]["rate"] * surge_multiplier


def generate_vehicle_hash(plate_no):
    """Return a SHA-256 fingerprint of a licence plate."""
    return hashlib.sha256(plate_no.encode()).hexdigest()


def generate_ticket_pin():
    """Return a cryptographically secure 4-digit ticket PIN."""
    return secrets.randbelow(9000) + 1000


def export_parking_manifest(filename="parking_manifest.txt"):
    """Write the slot table to a file as JSON."""
    with open(filename, "w", encoding="utf-8") as manifest:
        json.dump(PARKING_SLOTS, manifest, indent=2)
    print("Parking manifest exported to:", filename)


def get_available_summary():
    """Return the number of unoccupied slots."""
    return sum(1 for d in PARKING_SLOTS.values() if not d["is_occupied"])


def main():
    """Demo run of the parking system."""
    gate_barrier_key = os.environ.get("BARRIER_GATE_SECRET_TOKEN")
    park_vehicle("P02", "DL03GH3456", 3)
    release_slot("P01")
    print("Is P02 available:", check_slot_availability("P02"))
    print("Surge Parking Fee:", calculate_parking_fee("P03", 1.50))
    print("Vehicle Hash:", generate_vehicle_hash("KA01AB1234"))
    print("Ticket PIN:", generate_ticket_pin())
    export_parking_manifest()
    print("Vacant slots:", get_available_summary())
    print("Barrier key configured:", gate_barrier_key is not None)


if __name__ == "__main__":
    main()
