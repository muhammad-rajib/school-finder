import random
import sys
from datetime import date, timedelta
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.db.session import SessionLocal
from app.models.notice import Notice
from app.models.result import Result
from app.models.school import School
from app.models.school_image import SchoolImage
from app.models.teacher import Teacher


random.seed(42)

LOCATION_DATA = [
    ("Dhaka", "Dhaka", "Savar", "Ashulia"),
    ("Dhaka", "Dhaka", "Keraniganj", "Kalatia"),
    ("Dhaka", "Gazipur", "Kaliganj", "Tumlia"),
    ("Dhaka", "Gazipur", "Sreepur", "Mawna"),
    ("Dhaka", "Gazipur", "Kapasia", "Tokra"),
    ("Chattogram", "Chattogram", "Patiya", "Kusumpura"),
    ("Chattogram", "Chattogram", "Sitakunda", "Sonaichhari"),
    ("Chattogram", "Chattogram", "Anwara", "Barakhain"),
    ("Chattogram", "Cox's Bazar", "Ramu", "Garjoniya"),
    ("Chattogram", "Cox's Bazar", "Chakaria", "Dulahazara"),
    ("Rajshahi", "Rajshahi", "Paba", "Harian"),
    ("Rajshahi", "Rajshahi", "Bagha", "Arani"),
    ("Rajshahi", "Rajshahi", "Durgapur", "Maria"),
    ("Rajshahi", "Bogura", "Dupchanchia", "Talora"),
    ("Rajshahi", "Bogura", "Sherpur", "Mirzapur"),
    ("Khulna", "Jessore", "Jhikargacha", "Bankra"),
    ("Khulna", "Khulna", "Batiaghata", "Gangarampur"),
    ("Barishal", "Barishal", "Banaripara", "Bisharkandi"),
    ("Sylhet", "Sylhet", "Beanibazar", "Mathiura"),
    ("Rangpur", "Dinajpur", "Birganj", "Mohonpur"),
]

SCHOOL_PREFIXES = [
    "Greenfield",
    "Sunrise",
    "Scholars",
    "Ideal",
    "Progressive",
    "Bright Future",
    "Little Blossoms",
    "Shapla",
    "Golden Valley",
    "Harmony",
    "Udayan",
    "Monihar",
    "Blue Sky",
    "Crescent",
    "Northern Star",
    "Evergreen",
    "South Point",
    "Riverdale",
    "Heritage",
    "Morning Dew",
]

TEACHER_NAMES = [
    "Ayesha Rahman",
    "Karim Uddin",
    "Nusrat Jahan",
    "Farhana Islam",
    "Mahmud Hasan",
    "Sharmin Akter",
    "Tanvir Ahmed",
    "Sadia Afrin",
    "Rakib Hossain",
    "Mst. Rupa Begum",
]

SUBJECTS = [
    "Bangla",
    "English",
    "Mathematics",
    "Science",
    "Social Science",
    "ICT",
    "Religion",
]

QUALIFICATIONS = [
    "B.Ed, M.Ed",
    "BSc, MEd",
    "MA in Education",
    "BA, B.Ed",
    "MSc, B.Ed",
]

NOTICE_TOPICS = [
    ("Admission Notice", "Admission forms are available for the upcoming academic session."),
    ("Holiday Notice", "The school will remain closed due to a public holiday."),
    ("Exam Schedule", "Term examination schedule has been published for all classes."),
    ("Guardian Meeting", "A parent-teacher meeting will be held on campus this week."),
]

EXAM_TYPES = ["PSC", "PEC", "JSC", "SSC"]


def random_phone() -> str:
    return f"+8801{random.randint(3, 9)}{random.randint(10000000, 99999999)}"


def random_email(school_name: str) -> str:
    slug = school_name.lower().replace(" ", "-").replace("&", "and")
    return f"info@{slug}.edu.bd"


def random_website(school_name: str) -> str:
    slug = school_name.lower().replace(" ", "-").replace("&", "and")
    return f"https://{slug}.schoolfinder.test"


def build_school(index: int) -> School:
    division, district, upazila, union_name = LOCATION_DATA[index % len(LOCATION_DATA)]
    prefix = SCHOOL_PREFIXES[index % len(SCHOOL_PREFIXES)]
    school_name = f"{prefix} Primary School {index + 1}"
    total_students = random.randint(280, 950)
    boys = random.randint(total_students // 2 - 40, total_students // 2 + 40)
    boys = max(120, min(boys, total_students - 100))
    girls = total_students - boys
    total_teachers = random.randint(3, 5)

    return School(
        emis_code=f"BD{2026}{index + 1:04d}",
        name=school_name,
        country_code="BD",
        division=division,
        district=district,
        upazila=upazila,
        union=union_name,
        address=f"{union_name}, {upazila}, {district}",
        description=(
            f"{school_name} is a community-focused primary school serving families in "
            f"{union_name}, {upazila}. The school emphasizes foundational literacy, "
            "inclusive learning, and strong family engagement."
        ),
        phone=random_phone(),
        email=random_email(school_name),
        website=random_website(school_name),
        established_year=random.randint(1985, 2016),
        total_students=total_students,
        boys=boys,
        girls=girls,
        total_teachers=total_teachers,
        total_classrooms=random.randint(8, 22),
        has_electricity=random.choice([True, True, True, False]),
        has_water=random.choice([True, True, True, False]),
    )


def build_teachers(school: School) -> list[Teacher]:
    teacher_count = school.total_teachers
    used_names = random.sample(TEACHER_NAMES, k=teacher_count)
    teachers: list[Teacher] = []

    for index, name in enumerate(used_names):
        teachers.append(
            Teacher(
                school_id=school.id,
                name=name,
                designation="Head Teacher" if index == 0 else "Assistant Teacher",
                subject=random.choice(SUBJECTS),
                qualification=random.choice(QUALIFICATIONS),
                phone=random_phone(),
                joining_date=date.today() - timedelta(days=random.randint(300, 5000)),
            )
        )

    return teachers


def build_results(school: School) -> list[Result]:
    years = random.sample([2022, 2023, 2024, 2025], k=random.randint(2, 3))
    results: list[Result] = []

    for year in sorted(years):
        results.append(
            Result(
                school_id=school.id,
                year=year,
                exam_type=random.choice(EXAM_TYPES),
                pass_rate=round(random.uniform(72.0, 99.2), 2),
            )
        )

    return results


def build_notices(school: School) -> list[Notice]:
    notices: list[Notice] = []

    for index in range(2):
        title, description = NOTICE_TOPICS[(school.established_year + index) % len(NOTICE_TOPICS)]
        notices.append(
            Notice(
                school_id=school.id,
                title=title,
                description=f"{description} This update is for {school.name}.",
                published_date=date.today() - timedelta(days=random.randint(1, 90)),
            )
        )

    return notices


def build_images(school: School) -> list[SchoolImage]:
    image_count = random.randint(2, 3)
    images: list[SchoolImage] = []

    for index in range(image_count):
        images.append(
            SchoolImage(
                school_id=school.id,
                image_url=f"https://picsum.photos/seed/{school.id}-{index}/800/400",
                is_cover=index == 0,
            )
        )

    return images


def seed_data() -> None:
    session = SessionLocal()

    try:
        existing_school_count = session.query(School).count()
        if existing_school_count >= 20:
            return

        schools_to_create = 20 - existing_school_count

        for index in range(existing_school_count, existing_school_count + schools_to_create):
            school = build_school(index)
            session.add(school)
            session.flush()

            teachers = build_teachers(school)
            results = build_results(school)
            notices = build_notices(school)
            images = build_images(school)

            session.add_all(teachers + results + notices + images)

        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_data()
