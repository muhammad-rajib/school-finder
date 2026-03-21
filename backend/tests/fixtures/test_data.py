from datetime import date, datetime, timezone
from types import SimpleNamespace
from uuid import uuid4


def build_school_data(**overrides: object) -> dict[str, object]:
    school = {
        "id": str(uuid4()),
        "emis_code": "123456",
        "name": "Sample School",
        "country_code": "BD",
        "division": "Dhaka",
        "district": "Dhaka",
        "upazila": "Dhanmondi",
        "union": "Ward 1",
        "address": "Road 1, Dhaka",
        "description": "A leading secondary school in central Dhaka.",
        "phone": "+8801712345678",
        "email": "info@sample-school.edu",
        "website": "https://sample-school.edu",
        "established_year": 1998,
        "total_students": 500,
        "boys": 260,
        "girls": 240,
        "total_teachers": 25,
        "total_classrooms": 18,
        "has_electricity": True,
        "has_water": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    school.update(overrides)
    return school


def build_teacher_data(**overrides: object) -> dict[str, object]:
    teacher = {
        "id": str(uuid4()),
        "name": "Sample Teacher",
        "designation": "Assistant Teacher",
        "subject": "Mathematics",
        "qualification": "M.Sc. in Mathematics",
    }
    teacher.update(overrides)
    return teacher


def build_result_data(**overrides: object) -> dict[str, object]:
    result = {
        "year": 2025,
        "exam_type": "SSC",
        "pass_rate": 92.5,
    }
    result.update(overrides)
    return result


def build_notice_data(**overrides: object) -> dict[str, object]:
    notice = {
        "title": "Admission Notice",
        "description": "Class six admission forms are now available.",
        "published_date": date(2026, 3, 21).isoformat(),
    }
    notice.update(overrides)
    return notice


def build_school_image_data(**overrides: object) -> dict[str, object]:
    image = {
        "id": str(uuid4()),
        "image_url": "https://cdn.example.com/schools/cover.jpg",
        "is_cover": False,
    }
    image.update(overrides)
    return image


def build_user_data(**overrides: object) -> SimpleNamespace:
    user = {
        "id": uuid4(),
        "name": "Admin User",
        "email": "admin@example.com",
        "password_hash": "$2b$12$examplehash",
        "role": "admin",
        "school_id": None,
        "is_active": True,
    }
    user.update(overrides)
    return SimpleNamespace(**user)
