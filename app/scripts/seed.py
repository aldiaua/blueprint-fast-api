"""
Seed data script for teachers and classes tables.
Run with: python -m app.scripts.seed
"""

import asyncio

from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import AsyncSessionLocal
from app.models.base import Class, PageSection, Setting, Student, Teacher, User
from app.services.auth_service import AuthService


async def seed_teachers():
    """Insert sample teacher data into the database."""

    teachers_data = [
        {
            "name": "Dr. Budi Santoso",
            "position": "Kepala Sekolah",
            "subject": "Administrasi",
            "quote": "Pendidikan adalah investasi terbaik untuk masa depan.",
            "biography": "Dr. Budi Santoso merupakan pendidik berpengalaman lebih dari 20 tahun...",
            "photo": "/assets/teachers/budi-santoso.jpg",
            "email": "budi.santoso@example.com",
            "phone": "+62812-3456-7890",
            "instagram": "@budisantoso",
            "linkedin": "linkedin.com/in/budisantoso",
            "sort_order": 1,
            "is_active": True,
        },
        {
            "name": "Ibu Siti Nurhaliza",
            "position": "Wakil Kepala Sekolah",
            "subject": "Bahasa Indonesia",
            "quote": "Membaca adalah jendela ilmu.",
            "biography": "Ibu Siti Nurhaliza adalah guru berpengalaman dalam mengajar Bahasa Indonesia...",
            "photo": "/assets/teachers/siti-nurhaliza.jpg",
            "email": "siti.nurhaliza@example.com",
            "phone": "+62812-9876-5432",
            "instagram": "@sitihaliza",
            "linkedin": "linkedin.com/in/sitihaliza",
            "sort_order": 2,
            "is_active": True,
        },
        {
            "name": "Pak Ahmad Wijaya",
            "position": "Guru Matematika",
            "subject": "Matematika",
            "quote": "Matematika adalah bahasa universal.",
            "biography": "Pak Ahmad Wijaya mengajar matematika dengan metode yang inovatif dan menyenangkan...",
            "photo": "/assets/teachers/ahmad-wijaya.jpg",
            "email": "ahmad.wijaya@example.com",
            "phone": "+62812-1111-2222",
            "instagram": "@ahmadwijaya",
            "linkedin": "linkedin.com/in/ahmadwijaya",
            "sort_order": 3,
            "is_active": True,
        },
        {
            "name": "Ibu Ratna Dewi",
            "position": "Guru Fisika",
            "subject": "Fisika",
            "quote": "Sains adalah studi tentang alam.",
            "biography": "Ibu Ratna Dewi membuat eksperimen fisika yang engaging untuk siswa...",
            "photo": "/assets/teachers/ratna-dewi.jpg",
            "email": "ratna.dewi@example.com",
            "phone": "+62812-3333-4444",
            "instagram": "@ratnadewi",
            "linkedin": "linkedin.com/in/ratnadewi",
            "sort_order": 4,
            "is_active": True,
        },
        {
            "name": "Pak Rudi Hartono",
            "position": "Guru Kimia",
            "subject": "Kimia",
            "quote": "Kimia adalah kehidupan yang indah.",
            "biography": "Pak Rudi Hartono membuat kelas kimia menjadi lebih interaktif...",
            "photo": "/assets/teachers/rudi-hartono.jpg",
            "email": "rudi.hartono@example.com",
            "phone": "+62812-5555-6666",
            "instagram": "@rudihartono",
            "linkedin": "linkedin.com/in/rudihartono",
            "sort_order": 5,
            "is_active": True,
        },
        {
            "name": "Ibu Eka Putri",
            "position": "Guru Biologi",
            "subject": "Biologi",
            "quote": "Biologi adalah studi tentang kehidupan.",
            "biography": "Ibu Eka Putri mengajar biologi dengan fokus pada eksperimen lapangan...",
            "photo": "/assets/teachers/eka-putri.jpg",
            "email": "eka.putri@example.com",
            "phone": "+62812-7777-8888",
            "instagram": "@ekaputri",
            "linkedin": "linkedin.com/in/ekaputri",
            "sort_order": 6,
            "is_active": True,
        },
    ]

    async with AsyncSessionLocal() as session:
        try:
            # Check if teachers already exist
            result = await session.execute(select(func.count()).select_from(Teacher))
            count = result.scalar()

            if count > 0:
                print(
                    f"✅ Teachers: Database sudah berisi {count} record(s). Skip seeding."
                )
            else:
                # Insert teachers
                stmt = insert(Teacher).values(teachers_data)
                await session.execute(stmt)
                print(f"✅ Teachers: {len(teachers_data)} records inserted.")

            await session.commit()

        except Exception as e:
            await session.rollback()
            print(f"❌ Error during teacher seeding: {e}")
            raise


async def seed_classes():
    """Insert sample class data into the database."""

    classes_data = [
        {
            "name": "XII IPA 1",
            "slug": "xii-ipa-1",
            "description": "Kelas XII IPA dengan fokus pada ilmu alam dan teknologi.",
            "cover_image": "/assets/classes/xii-ipa-1.jpg",
            "homeroom_teacher_id": 1,
            "graduation_year": 2025,
            "sort_order": 1,
            "is_active": True,
        },
        {
            "name": "XII IPA 2",
            "slug": "xii-ipa-2",
            "description": "Kelas XII IPA dengan program akselerasi.",
            "cover_image": "/assets/classes/xii-ipa-2.jpg",
            "homeroom_teacher_id": 3,
            "graduation_year": 2025,
            "sort_order": 2,
            "is_active": True,
        },
        {
            "name": "XII IPS",
            "slug": "xii-ips",
            "description": "Kelas XII IPS dengan fokus pada ilmu sosial dan kemanusiaan.",
            "cover_image": "/assets/classes/xii-ips.jpg",
            "homeroom_teacher_id": 2,
            "graduation_year": 2025,
            "sort_order": 3,
            "is_active": True,
        },
        {
            "name": "XI IPA 1",
            "slug": "xi-ipa-1",
            "description": "Kelas XI IPA angkatan 2024.",
            "cover_image": "/assets/classes/xi-ipa-1.jpg",
            "homeroom_teacher_id": 4,
            "graduation_year": 2026,
            "sort_order": 4,
            "is_active": True,
        },
        {
            "name": "XI IPA 2",
            "slug": "xi-ipa-2",
            "description": "Kelas XI IPA dengan program unggulan.",
            "cover_image": "/assets/classes/xi-ipa-2.jpg",
            "homeroom_teacher_id": 5,
            "graduation_year": 2026,
            "sort_order": 5,
            "is_active": True,
        },
        {
            "name": "XI IPS",
            "slug": "xi-ips",
            "description": "Kelas XI IPS angkatan 2024.",
            "cover_image": "/assets/classes/xi-ips.jpg",
            "homeroom_teacher_id": 6,
            "graduation_year": 2026,
            "sort_order": 6,
            "is_active": True,
        },
    ]

    async with AsyncSessionLocal() as session:
        try:
            # Check if classes already exist
            result = await session.execute(select(func.count()).select_from(Class))
            count = result.scalar()

            if count > 0:
                print(
                    f"✅ Classes: Database sudah berisi {count} record(s). Skip seeding."
                )
            else:
                # Insert classes
                stmt = insert(Class).values(classes_data)
                await session.execute(stmt)
                print(f"✅ Classes: {len(classes_data)} records inserted.")

            await session.commit()

        except Exception as e:
            await session.rollback()
            print(f"❌ Error during class seeding: {e}")
            raise


async def seed_students():
    """Insert sample student data into the database."""

    students_data = [
        # XII IPA 1 - 4 students
        {
            "class_id": 1,
            "nis": "001",
            "full_name": "Andi Pratama",
            "nick_name": "Andi",
            "gender": "Laki-laki",
            "birth_place": "Jakarta",
            "birth_date": "2006-05-15",
            "address": "Jl. Merdeka No. 1, Jakarta",
            "hobby": "Bermain basket",
            "ambition": "Menjadi insinyur",
            "quote": "Kegigihan adalah kunci kesuksesan.",
            "photo": "/assets/students/andi-pratama.jpg",
            "instagram": "@andipratama",
            "tiktok": "@andipratama",
            "email": "andi.pratama@example.com",
            "phone": "+62812-0001-0001",
            "sort_order": 1,
            "is_active": True,
        },
        {
            "class_id": 1,
            "nis": "002",
            "full_name": "Budi Santoso",
            "nick_name": "Budi",
            "gender": "Laki-laki",
            "birth_place": "Bandung",
            "birth_date": "2006-08-22",
            "address": "Jl. Sudirman No. 2, Bandung",
            "hobby": "Bermain musik",
            "ambition": "Menjadi musisi profesional",
            "quote": "Musik adalah bahasa jiwa.",
            "photo": "/assets/students/budi-santoso.jpg",
            "instagram": "@budisantoso",
            "tiktok": "@budisantoso",
            "email": "budi.santoso@example.com",
            "phone": "+62812-0002-0002",
            "sort_order": 2,
            "is_active": True,
        },
        {
            "class_id": 1,
            "nis": "003",
            "full_name": "Citra Dewi",
            "nick_name": "Citra",
            "gender": "Perempuan",
            "birth_place": "Surabaya",
            "birth_date": "2006-03-10",
            "address": "Jl. Ahmad Yani No. 3, Surabaya",
            "hobby": "Membaca",
            "ambition": "Menjadi penulis",
            "quote": "Membaca adalah petualangan yang tak terlupakan.",
            "photo": "/assets/students/citra-dewi.jpg",
            "instagram": "@citradewi",
            "tiktok": "@citradewi",
            "email": "citra.dewi@example.com",
            "phone": "+62812-0003-0003",
            "sort_order": 3,
            "is_active": True,
        },
        {
            "class_id": 1,
            "nis": "004",
            "full_name": "Desi Wijaya",
            "nick_name": "Desi",
            "gender": "Perempuan",
            "birth_place": "Medan",
            "birth_date": "2006-11-05",
            "address": "Jl. Gatot Subroto No. 4, Medan",
            "hobby": "Melukis",
            "ambition": "Menjadi desainer grafis",
            "quote": "Seni adalah ekspresi jiwa.",
            "photo": "/assets/students/desi-wijaya.jpg",
            "instagram": "@desiwijaya",
            "tiktok": "@desiwijaya",
            "email": "desi.wijaya@example.com",
            "phone": "+62812-0004-0004",
            "sort_order": 4,
            "is_active": True,
        },
        # XII IPA 2 - 3 students
        {
            "class_id": 2,
            "nis": "005",
            "full_name": "Eka Prasetya",
            "nick_name": "Eka",
            "gender": "Laki-laki",
            "birth_place": "Yogyakarta",
            "birth_date": "2006-07-14",
            "address": "Jl. Malioboro No. 5, Yogyakarta",
            "hobby": "Coding",
            "ambition": "Menjadi software developer",
            "quote": "Code is poetry.",
            "photo": "/assets/students/eka-prasetya.jpg",
            "instagram": "@ekaprasetya",
            "tiktok": "@ekaprasetya",
            "email": "eka.prasetya@example.com",
            "phone": "+62812-0005-0005",
            "sort_order": 1,
            "is_active": True,
        },
        {
            "class_id": 2,
            "nis": "006",
            "full_name": "Farina Aziz",
            "nick_name": "Farina",
            "gender": "Perempuan",
            "birth_place": "Semarang",
            "birth_date": "2006-09-28",
            "address": "Jl. Pemuda No. 6, Semarang",
            "hobby": "Olahraga",
            "ambition": "Menjadi atlet profesional",
            "quote": "Olahraga adalah gaya hidup sehat.",
            "photo": "/assets/students/farina-aziz.jpg",
            "instagram": "@farinaazip",
            "tiktok": "@farinaazip",
            "email": "farina.aziz@example.com",
            "phone": "+62812-0006-0006",
            "sort_order": 2,
            "is_active": True,
        },
        {
            "class_id": 2,
            "nis": "007",
            "full_name": "Gita Kusuma",
            "nick_name": "Gita",
            "gender": "Perempuan",
            "birth_place": "Palembang",
            "birth_date": "2006-02-20",
            "address": "Jl. Pertamina No. 7, Palembang",
            "hobby": "Tari",
            "ambition": "Menjadi penari professional",
            "quote": "Tari adalah ekspresi indah.",
            "photo": "/assets/students/gita-kusuma.jpg",
            "instagram": "@gitakusuma",
            "tiktok": "@gitakusuma",
            "email": "gita.kusuma@example.com",
            "phone": "+62812-0007-0007",
            "sort_order": 3,
            "is_active": True,
        },
        # XII IPS - 3 students
        {
            "class_id": 3,
            "nis": "008",
            "full_name": "Hadi Sutrisno",
            "nick_name": "Hadi",
            "gender": "Laki-laki",
            "birth_place": "Makassar",
            "birth_date": "2006-06-12",
            "address": "Jl. Veteran No. 8, Makassar",
            "hobby": "Debat",
            "ambition": "Menjadi pengacara",
            "quote": "Hukum adalah fondasi keadilan.",
            "photo": "/assets/students/hadi-sutrisno.jpg",
            "instagram": "@hadisutrisno",
            "tiktok": "@hadisutrisno",
            "email": "hadi.sutrisno@example.com",
            "phone": "+62812-0008-0008",
            "sort_order": 1,
            "is_active": True,
        },
        {
            "class_id": 3,
            "nis": "009",
            "full_name": "Intan Permata",
            "nick_name": "Intan",
            "gender": "Perempuan",
            "birth_place": "Banjarmasin",
            "birth_date": "2006-10-08",
            "address": "Jl. Diponegoro No. 9, Banjarmasin",
            "hobby": "Menulis",
            "ambition": "Menjadi jurnalis",
            "quote": "Pena lebih kuat dari pedang.",
            "photo": "/assets/students/intan-permata.jpg",
            "instagram": "@intanpermata",
            "tiktok": "@intanpermata",
            "email": "intan.permata@example.com",
            "phone": "+62812-0009-0009",
            "sort_order": 2,
            "is_active": True,
        },
        {
            "class_id": 3,
            "nis": "010",
            "full_name": "Joko Wardana",
            "nick_name": "Joko",
            "gender": "Laki-laki",
            "birth_place": "Pontianak",
            "birth_date": "2006-04-25",
            "address": "Jl. Tanjungpura No. 10, Pontianak",
            "hobby": "Politik",
            "ambition": "Menjadi politisi",
            "quote": "Negara yang baik dimulai dari rakyat yang baik.",
            "photo": "/assets/students/joko-wardana.jpg",
            "instagram": "@jokowardana",
            "tiktok": "@jokowardana",
            "email": "joko.wardana@example.com",
            "phone": "+62812-0010-0010",
            "sort_order": 3,
            "is_active": True,
        },
    ]

    async with AsyncSessionLocal() as session:
        try:
            # Check if students already exist
            result = await session.execute(select(func.count()).select_from(Student))
            count = result.scalar()

            if count > 0:
                print(
                    f"✅ Students: Database sudah berisi {count} record(s). Skip seeding."
                )
            else:
                # Insert students
                stmt = insert(Student).values(students_data)
                await session.execute(stmt)
                print(f"✅ Students: {len(students_data)} records inserted.")

            await session.commit()

        except Exception as e:
            await session.rollback()
            print(f"❌ Error during student seeding: {e}")
            raise


async def seed_settings():
    """Insert sample settings data into the database."""

    settings_data = [
        {
            "setting_key": "website",
            "components": {
                "name": "Yearbook SMA",
                "tagline": "Kenang-kenangan digital sekolah",
                "description": "Website kenang-kenangan tahun ajaran",
                "logo": "/assets/logo.png",
                "favicon": "/assets/favicon.ico",
            },
            "styles": {
                "primary_color": "#1e3a8a",
                "secondary_color": "#7c3aed",
                "font_family": "Poppins",
            },
            "description": "Website Information",
        },
        {
            "setting_key": "header",
            "components": {
                "logo": "/assets/logo.png",
                "logo_text": "Yearbook",
                "menu": [
                    {"label": "Home", "url": "/"},
                    {"label": "Classes", "url": "/classes"},
                    {"label": "Teachers", "url": "/teachers"},
                    {"label": "Gallery", "url": "/gallery"},
                ],
            },
            "styles": {
                "background": "white",
                "text_color": "#000",
                "border_bottom": "1px solid #e5e7eb",
            },
            "description": "Header Configuration",
        },
        {
            "setting_key": "footer",
            "components": {
                "text": "© 2025 Yearbook. All rights reserved.",
                "links": [
                    {"label": "Privacy Policy", "url": "/privacy"},
                    {"label": "Terms of Service", "url": "/terms"},
                    {"label": "Contact", "url": "/contact"},
                ],
                "copyright_year": 2025,
            },
            "styles": {
                "background": "#1f2937",
                "text_color": "#f3f4f6",
            },
            "description": "Footer Configuration",
        },
        {
            "setting_key": "seo",
            "components": {
                "site_title": "Yearbook SMA",
                "site_description": "Website kenang-kenangan digital sekolah menengah atas",
                "keywords": ["yearbook", "sekolah", "kenang-kenangan", "siswa"],
                "og_image": "/assets/og-image.png",
            },
            "styles": {},
            "description": "SEO Configuration",
        },
        {
            "setting_key": "social",
            "components": {
                "facebook": "https://facebook.com/yearbook",
                "instagram": "https://instagram.com/yearbook",
                "twitter": "https://twitter.com/yearbook",
                "tiktok": "https://tiktok.com/@yearbook",
                "youtube": "https://youtube.com/yearbook",
            },
            "styles": {},
            "description": "Social Media Configuration",
        },
        {
            "setting_key": "theme",
            "components": {
                "mode": "light",
                "layout": "default",
                "sidebar": True,
            },
            "styles": {
                "border_radius": "8px",
                "shadow": "0 1px 3px rgba(0, 0, 0, 0.1)",
                "transition": "all 0.3s ease",
            },
            "description": "Theme Configuration",
        },
    ]

    async with AsyncSessionLocal() as session:
        try:
            # Check if settings already exist
            result = await session.execute(select(func.count()).select_from(Setting))
            count = result.scalar()

            if count > 0:
                print(
                    f"✅ Settings: Database sudah berisi {count} record(s). Skip seeding."
                )
            else:
                # Insert settings
                stmt = insert(Setting).values(settings_data)
                await session.execute(stmt)
                print(f"✅ Settings: {len(settings_data)} records inserted.")

            await session.commit()

        except Exception as e:
            await session.rollback()
            print(f"❌ Error during settings seeding: {e}")
            raise


async def seed_page_sections():
    """Insert sample page section data into the database."""
    page_sections_data = [
        {
            "section_type": "cover",
            "title": "Cover",
            "components": {
                "title": "Selamat Datang di Yearbook SMA",
                "subtitle": "Kenang-kenangan digital untuk generasi kita",
                "description": "Tampilkan momen terbaik, prestasi, dan cerita siswa dalam satu halaman.",
                "buttons": [
                    {"label": "Lihat Kelas", "url": "/classes"},
                    {"label": "Hubungi Kami", "url": "/contact"},
                ],
                "images": [{"url": "/assets/cover-hero.jpg", "alt": "Cover Yearbook"}],
            },
            "styles": {
                "background": {"color": "#f8fafc", "image": "/assets/cover-bg.jpg"},
                "spacing": {"top": 80, "bottom": 80},
                "animation": "fade-up",
            },
            "sort_order": 1,
            "is_active": True,
        },
        {
            "section_type": "principal",
            "title": "Principal Greeting",
            "components": {
                "heading": "Sambutan Kepala Sekolah",
                "message": "Selamat datang di halaman tahun kenangan kami. Semoga semua kenangan ini membawa inspirasi bagi generasi berikutnya.",
                "name": "Dr. Budi Santoso",
                "position": "Kepala Sekolah",
                "photo": "/assets/principal.jpg",
            },
            "styles": {
                "background": {"color": "#ffffff"},
                "spacing": {"top": 60, "bottom": 60},
                "container": "container",
            },
            "sort_order": 2,
            "is_active": True,
        },
        {
            "section_type": "teachers",
            "title": "Teachers",
            "components": {
                "heading": "Guru Unggulan",
                "description": "Tim pengajar yang berdedikasi dan inspiratif.",
                "items": [],
            },
            "styles": {
                "background": {"color": "#f1f5f9"},
                "spacing": {"top": 60, "bottom": 60},
                "animation": "fade-up",
            },
            "sort_order": 3,
            "is_active": True,
        },
        {
            "section_type": "generation",
            "title": "Generation",
            "components": {
                "heading": "Generasi Terbaik",
                "description": "Mengenang perjalanan dan pencapaian siswa dalam satu generasi.",
                "statistics": [
                    {"label": "Siswa", "value": 120},
                    {"label": "Kelas", "value": 6},
                    {"label": "Guru", "value": 18},
                ],
            },
            "styles": {
                "background": {"color": "#ffffff"},
                "spacing": {"top": 60, "bottom": 60},
                "container": "container",
            },
            "sort_order": 4,
            "is_active": True,
        },
        {
            "section_type": "classes",
            "title": "Classes",
            "components": {
                "heading": "Kelas Kami",
                "description": "Beberapa pilihan kelas dengan program unggulan dan ekstrakurikuler.",
                "items": [],
            },
            "styles": {
                "background": {"color": "#f8fafc"},
                "spacing": {"top": 60, "bottom": 60},
                "animation": "fade-up",
            },
            "sort_order": 5,
            "is_active": True,
        },
        {
            "section_type": "gallery",
            "title": "Gallery",
            "components": {
                "heading": "Galeri Momen",
                "description": "Potret kegiatan dan kenangan yang tak terlupakan.",
                "items": [
                    {"image": "/assets/gallery-1.jpg", "caption": "Upacara kelulusan"},
                    {
                        "image": "/assets/gallery-2.jpg",
                        "caption": "Kegiatan ekstrakurikuler",
                    },
                ],
            },
            "styles": {
                "background": {"color": "#ffffff"},
                "spacing": {"top": 60, "bottom": 60},
                "animation": "fade-up",
            },
            "sort_order": 6,
            "is_active": True,
        },
    ]

    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(
                select(func.count()).select_from(PageSection)
            )
            count = result.scalar()

            if count > 0:
                print(
                    f"✅ PageSections: Database sudah berisi {count} record(s). Skip seeding."
                )
            else:
                stmt = insert(PageSection).values(page_sections_data)
                await session.execute(stmt)
                print(f"✅ PageSections: {len(page_sections_data)} records inserted.")

            await session.commit()

        except Exception as e:
            await session.rollback()
            print(f"❌ Error during page section seeding: {e}")
            raise


async def seed_users():
    """Insert superadmin user for CMS access."""
    users_data = [
        {
            "username": "superadmin",
            "email": "superadmin@example.com",
            "password_hash": AuthService.get_password_hash("superadmin123"),
            "full_name": "Super Administrator",
            "role": "superadmin",
            "is_active": True,
        },
    ]

    async with AsyncSessionLocal() as session:
        try:
            # Check if users already exist
            result = await session.execute(select(func.count()).select_from(User))
            count = result.scalar()

            if count > 0:
                print(
                    f"✅ Users: Database sudah berisi {count} record(s). Skip seeding."
                )
            else:
                # Insert users
                stmt = insert(User).values(users_data)
                await session.execute(stmt)
                print(f"✅ Users: {len(users_data)} records inserted.")

            await session.commit()

        except Exception as e:
            await session.rollback()
            print(f"❌ Error during user seeding: {e}")
            raise


async def main():
    """Run all seed functions."""
    print("🌱 Starting seed process...")
    await seed_teachers()
    await seed_classes()
    await seed_students()
    await seed_page_sections()
    await seed_settings()
    await seed_users()
    print("✨ Seed process completed!")


if __name__ == "__main__":
    asyncio.run(main())
