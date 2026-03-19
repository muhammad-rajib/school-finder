import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.session import SessionLocal
from app.models.school import School


SAMPLE_SCHOOLS = [
    {
        "emis_code": "1201001",
        "name": "Dhaka Central High School",
        "division": "Dhaka",
        "district": "Dhaka",
        "upazila": "Dhanmondi",
        "address": "32 Dhanmondi, Dhaka",
        "total_students": 1800,
        "total_teachers": 65,
    },
    {
        "emis_code": "1201002",
        "name": "Chattogram Model School",
        "division": "Chattogram",
        "district": "Chattogram",
        "upazila": "Pahartali",
        "address": "Pahartali Road, Chattogram",
        "total_students": 1450,
        "total_teachers": 52,
    },
    {
        "emis_code": "1201003",
        "name": "Rajshahi Government Girls School",
        "division": "Rajshahi",
        "district": "Rajshahi",
        "upazila": "Boalia",
        "address": "Zero Point, Rajshahi",
        "total_students": 1300,
        "total_teachers": 48,
    },
    {
        "emis_code": "1201004",
        "name": "Khulna Collegiate School",
        "division": "Khulna",
        "district": "Khulna",
        "upazila": "Sonadanga",
        "address": "Sonadanga Main Road, Khulna",
        "total_students": 1100,
        "total_teachers": 41,
    },
    {
        "emis_code": "1201005",
        "name": "Sylhet Science Academy",
        "division": "Sylhet",
        "district": "Sylhet",
        "upazila": "Beanibazar",
        "address": "College Road, Sylhet",
        "total_students": 980,
        "total_teachers": 36,
    },
    {
        "emis_code": "1201006",
        "name": "Barishal Public School",
        "division": "Barishal",
        "district": "Barishal",
        "upazila": "Kotwali",
        "address": "Band Road, Barishal",
        "total_students": 890,
        "total_teachers": 32,
    },
    {
        "emis_code": "1201007",
        "name": "Rangpur Ideal School",
        "division": "Rangpur",
        "district": "Rangpur",
        "upazila": "Mithapukur",
        "address": "Station Road, Rangpur",
        "total_students": 1025,
        "total_teachers": 38,
    },
    {
        "emis_code": "1201008",
        "name": "Mymensingh Scholars School",
        "division": "Mymensingh",
        "district": "Mymensingh",
        "upazila": "Trishal",
        "address": "Town Hall Road, Mymensingh",
        "total_students": 1200,
        "total_teachers": 44,
    },
]


def seed_schools() -> None:
    db = SessionLocal()
    try:
        existing_emis_codes = {
            emis_code for (emis_code,) in db.query(School.emis_code).all()
        }
        new_schools = [
            School(**school)
            for school in SAMPLE_SCHOOLS
            if school["emis_code"] not in existing_emis_codes
        ]

        if not new_schools:
            print("No new schools inserted. Sample data already exists.")
            return

        db.add_all(new_schools)
        db.commit()
        print(f"Inserted {len(new_schools)} sample schools.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_schools()
