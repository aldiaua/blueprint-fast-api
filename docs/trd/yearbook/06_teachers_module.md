# Technical Requirement Document (TRD)

# 06. Teachers Module

| Document | Teachers |
| -------- | -------- |
| Version  | 1.0.0    |
| Status   | Draft    |
| Module   | Teachers |

---

# 1. Overview

Teacher Module digunakan untuk mengelola seluruh data guru yang akan ditampilkan pada halaman Guru.

Data guru merupakan Master Data sehingga disimpan pada tabel tersendiri dan bukan JSONB.

Section Guru pada Landing Page hanya mengambil data dari tabel teachers berdasarkan sort_order.

---

# 2. Objectives

Module ini bertujuan untuk:

- CRUD Guru
- Menampilkan daftar guru
- Mengatur urutan guru
- Mengatur publish guru
- Menjadi sumber data halaman Guru

---

# 3. UI Analysis

Berdasarkan HTML Template.

Teacher Section terdiri dari:

```

Section Header

↓

Teacher Grid

↓

Teacher Card

├── Photo

├── Name

├── Position

└── Detail Button

```

Administrator hanya mengelola data guru.

Layout diatur oleh page_sections.

---

# 4. Database

Table

teachers

| Column     | Type         | Nullable | Description  |
| ---------- | ------------ | -------- | ------------ |
| id         | BIGSERIAL    | NO       | PK           |
| uuid       | UUID         | NO       | Public UUID  |
| name       | VARCHAR(150) | NO       | Teacher Name |
| position   | VARCHAR(150) | NO       | Position     |
| subject    | VARCHAR(150) | YES      | Subject      |
| quote      | TEXT         | YES      | Quote        |
| biography  | TEXT         | YES      | Biography    |
| photo      | TEXT         | YES      | Photo URL    |
| email      | VARCHAR(150) | YES      | Email        |
| phone      | VARCHAR(50)  | YES      | Phone        |
| instagram  | VARCHAR(255) | YES      | Instagram    |
| linkedin   | VARCHAR(255) | YES      | LinkedIn     |
| sort_order | INTEGER      | NO       | Order        |
| is_active  | BOOLEAN      | NO       | Publish      |
| created_at | TIMESTAMP    | NO       | Created      |
| updated_at | TIMESTAMP    | NO       | Updated      |

---

# 5. UI Mapping

| HTML             | Database |
| ---------------- | -------- |
| Teacher Image    | photo    |
| Teacher Name     | name     |
| Teacher Position | position |
| Teacher Subject  | subject  |
| Quote            | quote    |

---

# 6. Business Rules

- Nama wajib unik.
- Position wajib diisi.
- Sort Order tidak boleh sama.
- Guru nonaktif tidak muncul di Public API.
- Foto bersifat opsional.
- Biography mendukung HTML.

---

# 7. Public API

## List Teachers

GET

/api/v1/teachers

Query

page

limit

search

Response

```json
{
    "success": true,
    "message": "Success",
    "data": [
        {
            "uuid": "",
            "name": "",
            "position": "",
            "subject": "",
            "photo": ""
        }
    ]
}
```

---

## Detail

GET

/api/v1/teachers/{uuid}

---

# 8. CMS API

GET

/api/v1/cms/teachers

GET

/api/v1/cms/teachers/{uuid}

POST

/api/v1/cms/teachers

PUT

/api/v1/cms/teachers/{uuid}

DELETE

/api/v1/cms/teachers/{uuid}

---

# 9. Create Request

```json
{
    "name": "",

    "position": "",

    "subject": "",

    "quote": "",

    "biography": "",

    "photo": "",

    "email": "",

    "phone": "",

    "instagram": "",

    "linkedin": "",

    "sort_order": 1,

    "is_active": true
}
```

---

# 10. Response

```json
{
    "success": true,

    "message": "Teacher created.",

    "data": {
        "uuid": ""
    }
}
```

---

# 11. Validation

| Field      | Rule     |
| ---------- | -------- |
| name       | Required |
| position   | Required |
| subject    | Optional |
| quote      | Optional |
| biography  | Optional |
| photo      | Optional |
| email      | Email    |
| phone      | Optional |
| sort_order | Required |
| is_active  | Boolean  |

---

# 12. Repository

TeacherRepository

Method

findAll()

findByUUID()

create()

update()

delete()

search()

---

# 13. Service

TeacherService

Method

getTeachers()

getTeacher()

createTeacher()

updateTeacher()

deleteTeacher()

---

# 14. Schema

TeacherCreateRequest

TeacherUpdateRequest

TeacherResponse

TeacherListResponse

---

# 15. Migration

```sql
CREATE TABLE teachers (

id BIGSERIAL PRIMARY KEY,

uuid UUID UNIQUE NOT NULL,

name VARCHAR(150) NOT NULL,

position VARCHAR(150) NOT NULL,

subject VARCHAR(150),

quote TEXT,

biography TEXT,

photo TEXT,

email VARCHAR(150),

phone VARCHAR(50),

instagram VARCHAR(255),

linkedin VARCHAR(255),

sort_order INTEGER NOT NULL,

is_active BOOLEAN DEFAULT TRUE,

created_at TIMESTAMP NOT NULL,

updated_at TIMESTAMP NOT NULL

);
```

---

# 16. Seeder

Seeder mengikuti data HTML.

Seluruh data guru akan dimasukkan.

Nama

Jabatan

Foto

Quote

Urutan

harus sama persis dengan template.

---

# 17. Testing

Positive

✓ Create Teacher

✓ Update Teacher

✓ Delete Teacher

✓ Get Teacher

✓ Search Teacher

Negative

✓ Duplicate Name

✓ Empty Position

✓ Invalid Email

✓ Invalid UUID

✓ Invalid Sort Order

---

# 18. Performance

List Guru menggunakan pagination.

Default

page = 1

limit = 20

Sorting

sort_order ASC

---

# 19. Future Improvement

- Filter berdasarkan Subject
- Teacher Achievement
- Teacher Experience
- Teacher Certification
- Favorite Teacher
- Teacher Detail Page
- Teacher Award
- Export Excel
- Import Excel
