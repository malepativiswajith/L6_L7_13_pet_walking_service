
import math


def parse_walk_schedule(schedule_spec):
    # Validate input type
    if not isinstance(schedule_spec, str):
        return None

    # Validate schedule format
    parts = schedule_spec.strip().split("-")

    if len(parts) != 3:
        return None

    pets_str, mins_str, weekend_str = parts

    # Validate numeric values
    try:
        pets = int(pets_str.strip())
        mins = int(mins_str.strip())
    except (ValueError, TypeError, OverflowError):
        return None

    # Validate pet count and duration
    if pets <= 0 or mins <= 0:
        return None

    # Validate weekend value
    weekend_map = {
        "YES": 15.0,
        "NO": 0.0
    }

    weekend_code = weekend_str.strip().upper()

    if weekend_code not in weekend_map:
        return None

    weekend_fee = weekend_map[weekend_code]

    # Calculate total fee
    base_fee = 20.0 if mins <= 30 else 35.0
    total = base_fee + (pets * 5.0) + weekend_fee

    return f"Walk: {pets} pets, {mins} mins - Total ${total:.2f}"


def compute_pace_per_pet(walk_metrics_str):
    # Validate input type
    if not isinstance(walk_metrics_str, str):
        return None

    # Validate input format
    parts = walk_metrics_str.strip().split("/")

    if len(parts) != 2:
        return None

    mins_str, pets_str = parts

    # Convert to numeric values
    try:
        mins = float(mins_str.strip())
        pets = float(pets_str.strip())
    except (ValueError, TypeError, OverflowError):
        return None

    # Reject invalid, infinite and negative values
    if not math.isfinite(mins) or not math.isfinite(pets):
        return None

    if mins < 0 or pets <= 0:
        return None

    # Calculate pace safely
    pace = mins / pets

    if not math.isfinite(pace):
        return None

    return round(pace, 2)


def lookup_temperament_surcharge(temperament_code):
    # Validate input type
    if not isinstance(temperament_code, str):
        return None

    prefix = temperament_code.strip().upper()[:3]

    surcharges = {
        "CAL": 0.0,
        "PLY": 5.0,
        "REA": 12.0,
        "AGG": 20.0
    }

    # Use safe dictionary lookup
    return surcharges.get(prefix)


def main():
    print("==== Running parse_walk_schedule ====")
    s_input = input("Enter schedule (e.g. 2-30-YES): ")
    print(parse_walk_schedule(s_input))

    print("\n==== Running compute_pace_per_pet ====")
    p_input = input("Enter minutes/pets (e.g. 45/3): ")
    print("Pace (min/pet):", compute_pace_per_pet(p_input))

    print("\n==== Running lookup_temperament_surcharge ====")
    t_input = input(
        "Enter temperament code (e.g. CALM, PLAYFUL, AGGRESSIVE): "
    )
    print("Surcharge: $", lookup_temperament_surcharge(t_input))


if __name__ == "__main__":
    main()

