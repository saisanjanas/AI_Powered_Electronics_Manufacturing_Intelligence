import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Reproducible random data
np.random.seed(42)

# Number of days to simulate
NUM_DAYS = 30

# Existing machine IDs
MACHINE_IDS = [1, 2, 3, 4, 5]

# Simulation start date
START_DATE = datetime(2026, 7, 20)

print("Data generation setup ready")
print(f"Machines: {MACHINE_IDS}")
print(f"Days: {NUM_DAYS}")

# -------------------------------
# Generate Production Data
# -------------------------------

production_data = []

production_id = 1

shifts = {
    "Morning": 8,
    "Afternoon": 8,
    "Night": 8
}

for day in range(NUM_DAYS):
    current_date = START_DATE + timedelta(days=day)

    for machine_id in MACHINE_IDS:

        for shift_name, production_hours in shifts.items():

            # Base production capacity differs by machine
            base_production = {
                1: 950,
                2: 900,
                3: 800,
                4: 980,
                5: 930
            }[machine_id]

            # Small random variation
            variation = np.random.normal(0, 40)

            units_produced = int(
                max(500, base_production + variation)
            )

            # Rejected units
            rejection_rate = np.random.uniform(0.01, 0.08)

            units_rejected = int(
                units_produced * rejection_rate
            )

            production_data.append({
                "production_id": production_id,
                "machine_id": machine_id,
                "production_date": current_date.date(),
                "shift": shift_name,
                "units_produced": units_produced,
                "units_rejected": units_rejected,
                "production_time_hours": production_hours
            })

            production_id += 1


production_df = pd.DataFrame(production_data)

print("\nProduction data generated successfully!")
print("Rows:", len(production_df))

print(production_df.head())


# -------------------------------
# Generate Production Targets
# -------------------------------

target_data = []

for _, row in production_df.iterrows():

    machine_id = row["machine_id"]

    base_target = {
        1: 1000,
        2: 900,
        3: 800,
        4: 1000,
        5: 950
    }[machine_id]

    # Small variation in daily target
    target_quantity = int(
        max(700, base_target + np.random.normal(0, 20))
    )

    target_data.append({
        "target_id": len(target_data) + 1,
        "machine_id": machine_id,
        "target_date": row["production_date"],
        "target_quantity": target_quantity
    })

production_targets_df = pd.DataFrame(target_data)

print("\nProduction target data generated successfully!")
print("Rows:", len(production_targets_df))

print(production_targets_df.head())


# -------------------------------
# Generate Quality Data
# -------------------------------

quality_data = []

defect_types = [
    "Solder Defect",
    "Component Misplacement",
    "PCB Damage",
    "Missing Component",
    "Overheating"
]

for _, row in production_df.iterrows():

    # Defect count is related to rejected units
    defect_count = int(
        max(1, row["units_rejected"] * np.random.uniform(0.15, 0.40))
    )

    # Higher defect count increases chance of failure
    if defect_count >= 15:
        quality_status = "Fail"
    else:
        quality_status = "Pass"

    quality_data.append({
        "quality_id": len(quality_data) + 1,
        "production_id": row["production_id"],
        "inspection_date": row["production_date"],
        "defect_type": np.random.choice(defect_types),
        "defect_count": defect_count,
        "quality_status": quality_status
    })

quality_df = pd.DataFrame(quality_data)

print("\nQuality data generated successfully!")
print("Rows:", len(quality_df))

print(quality_df.head())


# -------------------------------
# Generate Sensor Data
# -------------------------------

sensor_data = []

sensor_id = 1

for day in range(NUM_DAYS):

    current_date = START_DATE + timedelta(days=day)

    for machine_id in MACHINE_IDS:

        # Machine-specific base conditions
        base_temperature = {
            1: 70,
            2: 68,
            3: 82,
            4: 65,
            5: 67
        }[machine_id]

        base_vibration = {
            1: 3.0,
            2: 2.8,
            3: 5.0,
            4: 2.5,
            5: 2.7
        }[machine_id]

        # One temperature and vibration reading per shift
        for shift_index, hour in enumerate([8, 14, 22]):

            recorded_at = current_date + timedelta(hours=hour)

            temperature = round(
                base_temperature + np.random.normal(0, 3),
                2
            )

            vibration = round(
                max(0.5, base_vibration + np.random.normal(0, 0.5)),
                2
            )

            sensor_data.append({
                "sensor_id": sensor_id,
                "machine_id": machine_id,
                "sensor_type": "Temperature",
                "sensor_value": temperature,
                "unit": "°C",
                "recorded_at": recorded_at
            })

            sensor_id += 1

            sensor_data.append({
                "sensor_id": sensor_id,
                "machine_id": machine_id,
                "sensor_type": "Vibration",
                "sensor_value": vibration,
                "unit": "mm/s",
                "recorded_at": recorded_at
            })

            sensor_id += 1


sensors_df = pd.DataFrame(sensor_data)

print("\nSensor data generated successfully!")
print("Rows:", len(sensors_df))

print(sensors_df.head())


# -------------------------------
# Generate Downtime Data
# -------------------------------

downtime_data = []

downtime_id = 1

downtime_reasons = [
    "Material Shortage",
    "Machine Adjustment",
    "Mechanical Failure",
    "Testing Error",
    "Calibration",
    "Electrical Issue"
]

for day in range(NUM_DAYS):

    current_date = START_DATE + timedelta(days=day)

    for machine_id in MACHINE_IDS:

        # Base probability of downtime
        probability = {
            1: 0.20,
            2: 0.22,
            3: 0.40,
            4: 0.15,
            5: 0.18
        }[machine_id]

        if np.random.random() < probability:

            start_hour = np.random.randint(6, 22)

            downtime_start = current_date + timedelta(
                hours=int(start_hour)
            )

            downtime_hours = round(
                np.random.uniform(0.5, 4.0),
                2
            )

            downtime_end = downtime_start + timedelta(
                hours=downtime_hours
            )

            # Machine 3 has a higher chance of mechanical failure
            if machine_id == 3 and np.random.random() < 0.5:
                reason = "Mechanical Failure"
            else:
                reason = np.random.choice(downtime_reasons)

            downtime_data.append({
                "downtime_id": downtime_id,
                "machine_id": machine_id,
                "downtime_start": downtime_start,
                "downtime_end": downtime_end,
                "downtime_reason": reason,
                "downtime_hours": downtime_hours
            })

            downtime_id += 1


downtime_df = pd.DataFrame(downtime_data)

print("\nDowntime data generated successfully!")
print("Rows:", len(downtime_df))

print(downtime_df.head())


# -------------------------------
# Generate Maintenance Data
# -------------------------------

maintenance_data = []

maintenance_id = 1

maintenance_types = [
    "Preventive",
    "Routine Inspection",
    "Corrective"
]

maintenance_statuses = [
    "Completed",
    "Completed",
    "Completed",
    "In Progress"
]

for day in range(NUM_DAYS):

    current_date = START_DATE + timedelta(days=day)

    for machine_id in MACHINE_IDS:

        # Maintenance is more frequent for Machine 3
        probability = {
            1: 0.08,
            2: 0.08,
            3: 0.18,
            4: 0.06,
            5: 0.08
        }[machine_id]

        if np.random.random() < probability:

            maintenance_type = np.random.choice(
                maintenance_types,
                p=[0.45, 0.35, 0.20]
            )

            # Corrective maintenance takes longer and costs more
            if maintenance_type == "Corrective":
                downtime_hours = round(
                    np.random.uniform(3.0, 6.0), 2
                )
                maintenance_cost = round(
                    np.random.uniform(8000, 15000), 2
                )
            elif maintenance_type == "Preventive":
                downtime_hours = round(
                    np.random.uniform(1.0, 3.0), 2
                )
                maintenance_cost = round(
                    np.random.uniform(2500, 6000), 2
                )
            else:
                downtime_hours = round(
                    np.random.uniform(0.5, 2.0), 2
                )
                maintenance_cost = round(
                    np.random.uniform(1500, 4000), 2
                )

            maintenance_data.append({
                "maintenance_id": maintenance_id,
                "equipment_id": machine_id,
                "maintenance_date": current_date.date(),
                "maintenance_type": maintenance_type,
                "maintenance_status": np.random.choice(
                    maintenance_statuses
                ),
                "downtime_hours": downtime_hours,
                "maintenance_cost": maintenance_cost
            })

            maintenance_id += 1


maintenance_df = pd.DataFrame(maintenance_data)

print("\nMaintenance data generated successfully!")
print("Rows:", len(maintenance_df))

print(maintenance_df.head())

# -------------------------------
# Generate Production Logs
# -------------------------------

production_logs_data = []

log_id = 1

for _, row in production_df.iterrows():

    # Assign an employee based on the machine
    employee_id = ((int(row["machine_id"]) - 1) % 5) + 1

    production_logs_data.append({
        "log_id": log_id,
        "production_id": row["production_id"],
        "machine_id": row["machine_id"],
        "employee_id": employee_id,
        "log_date": row["production_date"],
        "quantity_produced": row["units_produced"]
    })

    log_id += 1


production_logs_df = pd.DataFrame(production_logs_data)

print("\nProduction logs generated successfully!")
print("Rows:", len(production_logs_df))

print(production_logs_df.head())

# -------------------------------
# Generate Shifts Data
# -------------------------------

shifts_data = []

shift_id = 1

shift_names = ["Morning", "Afternoon", "Night"]

for shift_name in shift_names:

    shifts_data.append({
        "shift_id": shift_id,
        "shift_name": shift_name,
        "start_time": {
            "Morning": "06:00:00",
            "Afternoon": "14:00:00",
            "Night": "22:00:00"
        }[shift_name],
        "end_time": {
            "Morning": "14:00:00",
            "Afternoon": "22:00:00",
            "Night": "06:00:00"
        }[shift_name],
        "supervisor": f"Supervisor {shift_id}"
    })

    shift_id += 1

shifts_df = pd.DataFrame(shifts_data)

print("\nShifts data generated successfully!")
print("Rows:", len(shifts_df))
print(shifts_df)

# -------------------------------
# Generate Employees Data
# -------------------------------

employees_data = []

roles = [
    "Machine Operator",
    "Quality Inspector",
    "Maintenance Technician",
    "Production Supervisor",
    "Technician"
]

departments = [
    "Production",
    "Quality",
    "Maintenance",
    "Production",
    "Maintenance"
]

for i in range(5):

    employees_data.append({
        "employee_id": i + 1,
        "employee_name": f"Employee {i + 1}",
        "department": departments[i],
        "role": roles[i],
        "shift": shift_names[i % 3]
    })

employees_df = pd.DataFrame(employees_data)

print("\nEmployees data generated successfully!")
print("Rows:", len(employees_df))
print(employees_df)

# -------------------------------
# Machine Reference Data
# -------------------------------

machines_df = pd.DataFrame([
    {
        "machine_id": 1,
        "machine_name": "PCB Assembly Line 01",
        "machine_type": "Assembly Line",
        "location": "Production Floor A",
        "status": "Operational",
        "installation_date": "2022-05-10"
    },
    {
        "machine_id": 2,
        "machine_name": "PCB Assembly Line 02",
        "machine_type": "Assembly Line",
        "location": "Production Floor A",
        "status": "Operational",
        "installation_date": "2022-08-15"
    },
    {
        "machine_id": 3,
        "machine_name": "CNC Precision Unit",
        "machine_type": "CNC Machine",
        "location": "Production Floor B",
        "status": "Maintenance",
        "installation_date": "2021-03-20"
    },
    {
        "machine_id": 4,
        "machine_name": "Testing Station 01",
        "machine_type": "Testing Equipment",
        "location": "Quality Floor",
        "status": "Operational",
        "installation_date": "2023-01-12"
    },
    {
        "machine_id": 5,
        "machine_name": "Testing Station 02",
        "machine_type": "Testing Equipment",
        "location": "Quality Floor",
        "status": "Operational",
        "installation_date": "2023-04-18"
    }
])

print("\nMachines data ready!")
print("Rows:", len(machines_df))

# -------------------------------
# Generate Inventory Data
# -------------------------------

# -------------------------------
# Generate Inventory Data
# -------------------------------

inventory_data = []

inventory_items = [
    ("PCB Boards", 5000, 1000, "pieces"),
    ("Resistors", 10000, 2000, "pieces"),
    ("Capacitors", 8000, 1600, "pieces"),
    ("Microcontrollers", 3000, 600, "pieces"),
    ("Solder Wire", 2000, 400, "kg")
]

for i, (material_name, quantity, reorder_level, unit) in enumerate(inventory_items):

    inventory_data.append({
        "inventory_id": i + 1,
        "material_name": material_name,
        "quantity_available": quantity,
        "reorder_level": reorder_level,
        "unit": unit,
        "last_updated": production_df["production_date"].max()
    })

inventory_df = pd.DataFrame(inventory_data)

print("\nInventory data generated successfully!")
print("Rows:", len(inventory_df))
print(inventory_df)
# -------------------------------
# Generate Suppliers Data
# -------------------------------

# -------------------------------
# Generate Suppliers Data
# -------------------------------

suppliers_data = []

supplier_materials = [
    "PCB Boards",
    "Resistors",
    "Capacitors",
    "Microcontrollers",
    "Solder Wire"
]

for i in range(5):

    suppliers_data.append({
        "supplier_id": i + 1,
        "supplier_name": f"Supplier {i + 1}",
        "material_supplied": supplier_materials[i],
        "contact_email": f"supplier{i + 1}@example.com",
        "contact_phone": f"900000000{i + 1}",
        "delivery_rating": round(
            np.random.uniform(3.5, 5.0), 2
        )
    })

suppliers_df = pd.DataFrame(suppliers_data)

print("\nSuppliers data generated successfully!")
print("Rows:", len(suppliers_df))
print(suppliers_df)

# -------------------------------
# Export Generated Data to CSV
# -------------------------------

from pathlib import Path

output_dir = Path(__file__).resolve().parent.parent / "data" / "generated"

output_dir.mkdir(parents=True, exist_ok=True)

datasets_to_export = {
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

for name, df in datasets_to_export.items():

    file_path = output_dir / f"{name}.csv"

    df.to_csv(file_path, index=False)

    print(f"Exported: {file_path}")

print("\nAll datasets exported successfully!")