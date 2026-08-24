import sys
from pathlib import Path

# Allow imports from src
sys.path.append(str(Path(__file__).resolve().parent))

from generate_data import (
    production_df,
    production_targets_df,
    quality_df,
    sensors_df,
    downtime_df,
    maintenance_df,
    production_logs_df,
    shifts_df,
    employees_df,
    machines_df,
    inventory_df,
    suppliers_df
)

datasets = {
    "production": production_df,
    "production_targets": production_targets_df,
    "quality": quality_df,
    "sensors": sensors_df,
    "downtime": downtime_df,
    "maintenance": maintenance_df,
    "production_logs": production_logs_df,
    "shifts": shifts_df,
    "employees": employees_df,
    "machines": machines_df,
    "inventory": inventory_df,
    "suppliers": suppliers_df
}

print("\n" + "=" * 70)
print("DATASET VALIDATION")
print("=" * 70)

for name, df in datasets.items():

    print(f"\n{name}")
    print("-" * 40)

    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Missing values:", df.isnull().sum().sum())
    print("Duplicate rows:", df.duplicated().sum())

    print("\n" + "=" * 70)
print("RELATIONSHIP VALIDATION")
print("=" * 70)

# Machines referenced in production
print(
    "\nProduction → Machines:",
    set(production_df["machine_id"]).issubset(
        set(machines_df["machine_id"])
    )
)

# Machines referenced in targets
print(
    "Production Targets → Machines:",
    set(production_targets_df["machine_id"]).issubset(
        set(machines_df["machine_id"])
    )
)

# Production referenced in quality
print(
    "Quality → Production:",
    set(quality_df["production_id"]).issubset(
        set(production_df["production_id"])
    )
)

# Production referenced in logs
print(
    "Production Logs → Production:",
    set(production_logs_df["production_id"]).issubset(
        set(production_df["production_id"])
    )
)

# Machines referenced in downtime
print(
    "Downtime → Machines:",
    set(downtime_df["machine_id"]).issubset(
        set(machines_df["machine_id"])
    )
)

# Machines referenced in sensors
print(
    "Sensors → Machines:",
    set(sensors_df["machine_id"]).issubset(
        set(machines_df["machine_id"])
    )
)

# Machines referenced in maintenance
print(
    "Maintenance → Machines:",
    set(maintenance_df["equipment_id"]).issubset(
        set(machines_df["machine_id"])
    )
)

# Suppliers referenced in inventory
print(
    "Inventory → Suppliers:",
    set(inventory_df["supplier_id"]).issubset(
        set(suppliers_df["supplier_id"])
    )
)


print("\n" + "=" * 70)
print("VALUE RANGE VALIDATION")
print("=" * 70)

checks = {
    "Production units produced > 0":
        (production_df["units_produced"] > 0).all(),

    "Production rejected >= 0":
        (production_df["units_rejected"] >= 0).all(),

    "Production time > 0":
        (production_df["production_time_hours"] > 0).all(),

    "Target quantity > 0":
        (production_targets_df["target_quantity"] > 0).all(),

    "Defect count >= 0":
        (quality_df["defect_count"] >= 0).all(),

    "Sensor values > 0":
        (sensors_df["sensor_value"] > 0).all(),

    "Downtime hours > 0":
        (downtime_df["downtime_hours"] > 0).all(),

    "Maintenance downtime >= 0":
        (maintenance_df["downtime_hours"] >= 0).all(),

    "Maintenance cost > 0":
        (maintenance_df["maintenance_cost"] > 0).all(),

    "Inventory quantity >= 0":
        (inventory_df["quantity_available"] >= 0).all(),

    "Delivery rating between 0 and 5":
        (
            (suppliers_df["delivery_rating"] >= 0) &
            (suppliers_df["delivery_rating"] <= 5)
        ).all()
}

for check, result in checks.items():
    print(f"{check}: {result}")