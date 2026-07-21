# Technical Requirement Document (TRD)

# 09. Students Module

| Document | Students    |
| -------- | ----------- |
| Version  | 1.0.0       |
| Status   | Draft       |
| Module   | Master Data |

---

# 1. Overview

Students merupakan Master Data yang menyimpan seluruh informasi siswa.

Setiap siswa harus terhubung dengan satu kelas.

Data ini digunakan oleh:

- Landing Page
- Detail Class
- Student Detail
- Search
- CMS

---

# 2. Objectives

Module ini bertujuan untuk:

- CRUD Siswa
- Menampilkan daftar siswa
- Menampilkan detail siswa
- Menampilkan siswa berdasarkan kelas
- Menjadi sumber data Yearbook

---

# 3. UI Analysis

Berdasarkan template HTML.

Student Card

```
Student Card

├── Photo

├── Full Name

├── Nickname

├── Quote

└── Detail Button
```

Detail Student

```
Student Detail

├── Cover

├── Photo

├── Full Name

├── Nickname

├── Birth Date

├── Address

├── Hobby

├── Dream

├── Quote

├── Social Media

└── Gallery
```

---

# 4. Database

Table

students

| Column      | Type         | Nullable | Description    |
| ----------- | ------------ | -------- | -------------- |
| id          | BIGSERIAL    | NO       | PK             |
| uuid        | UUID         | NO       | Public UUID    |
| class_id    | BIGINT       | NO       | FK Classes     |
| nis         | VARCHAR(50)  | YES      | Nomor Induk    |
| full_name   | VARCHAR(150) | NO       | Nama Lengkap   |
| nick_name   | VARCHAR(100) | YES      | Nama Panggilan |
| gender      | VARCHAR(10)  | YES      | Gender         |
| birth_place | VARCHAR(100) | YES      | Tempat Lahir   |
| birth_date  | DATE         | YES      | Tanggal Lahir  |
| address     | TEXT         | YES      | Alamat         |
| hobby       | VARCHAR(255) | YES      | Hobi           |
| ambition    | VARCHAR(255) | YES      | Cita-cita      |
| quote       | TEXT         | YES      | Quote          |
| photo       | TEXT         | YES      | Foto Profil    |
| cover_image | TEXT         | YES      | Cover          |
| instagram   | VARCHAR(255) | YES      | Instagram      |
| tiktok      | VARCHAR(255) | YES      | TikTok         |
| email       | VARCHAR(150) | YES      | Email          |
| phone       | VARCHAR(50)  | YES      | Nomor HP       |
| sort_order  | INTEGER      | NO       | Urutan         |
| is_active   | BOOLEAN      | NO       | Publish        |
| created_at  | TIMESTAMP    | NO       | Created        |
| updated_at  | TIMESTAMP    | NO       | Updated        |

---

# 5. Relationship

classes (1)

↓

students (N)

---

# 6. Business Rules

- Setiap siswa wajib memiliki kelas.
- Nama lengkap wajib diisi.
- Foto profil wajib ada.
- Cover image opsional.
- Quote opsional.
- Siswa nonaktif tidak tampil di Public API.
- Sort Order menentukan urutan pada halaman kelas.

---

# 7. Public API

## List Student

GET

/api/v1/students

Query

page

limit

search

class_uuid

---

## Detail Student

GET

/api/v1/students/{uuid}

---

## Student By Class

GET

/api/v1/classes/{class_uuid}/students

---

# 8. CMS API

GET

/api/v1/cms/students

GET

/api/v1/cms/students/{uuid}

POST

/api/v1/cms/students

PUT

/api/v1/cms/students/{uuid}

DELETE

/api/v1/cms/students/{uuid}

---

# 9. Create Request

```json
{
    "class_uuid": "",

    "nis": "",

    "full_name": "",

    "nick_name": "",

    "gender": "male",

    "birth_place": "",

    "birth_date": "2007-01-10",

    "address": "",

    "hobby": "",

    "ambition": "",

    "quote": "",

    "photo": "",

    "cover_image": "",

    "instagram": "",

    "tiktok": "",

    "email": "",

    "phone": "",

    "sort_order": 1,

    "is_active": true
}
```

---

# 10. Public Response

```json
{
    "success": true,
    "message": "Success",
    "data": {
        "uuid": "",
        "full_name": "",
        "nick_name": "",
        "photo": "",
        "quote": ""
    }
}
```

---

# 11. Detail Response

Selain data siswa, endpoint detail mengembalikan informasi kelas.

```json
{
    "uuid": "",

    "full_name": "",

    "photo": "",

    "quote": "",

    "class": {
        "uuid": "",

        "name": ""
    }
}
```

---

# 12. Validation

| Field      | Rule     |
| ---------- | -------- |
| class_uuid | Required |
| full_name  | Required |
| photo      | Required |
| nick_name  | Optional |
| quote      | Optional |
| birth_date | Optional |
| email      | Email    |
| sort_order | Required |

---

# 13. Repository

StudentRepository

Method

findAll()

findByUUID()

findByClass()

create()

update()

delete()

search()

---

# 14. Service

StudentService

Method

getStudents()

getStudent()

getStudentsByClass()

createStudent()

updateStudent()

deleteStudent()

---

# 15. Schema

StudentCreateRequest

StudentUpdateRequest

StudentResponse

StudentDetailResponse

StudentListResponse

---

# 16. Migration

```sql
CREATE TABLE students (

id BIGSERIAL PRIMARY KEY,

uuid UUID UNIQUE NOT NULL,

class_id BIGINT NOT NULL REFERENCES classes(id),

nis VARCHAR(50),

full_name VARCHAR(150) NOT NULL,

nick_name VARCHAR(100),

gender VARCHAR(10),

birth_place VARCHAR(100),

birth_date DATE,

address TEXT,

hobby VARCHAR(255),

ambition VARCHAR(255),

quote TEXT,

photo TEXT NOT NULL,

cover_image TEXT,

instagram VARCHAR(255),

tiktok VARCHAR(255),

email VARCHAR(150),

phone VARCHAR(50),

sort_order INTEGER NOT NULL,

is_active BOOLEAN DEFAULT TRUE,

created_at TIMESTAMP NOT NULL,

updated_at TIMESTAMP NOT NULL

);
```

---

# 17. Seeder

Data mengikuti template HTML.

Field yang disalin:

- Nama
- Foto
- Quote
- Cover
- Kelas
- Urutan

Seluruh asset menggunakan file yang sama dengan template HTML.

---

# 18. Testing

Positive

✓ Create Student

✓ Update Student

✓ Delete Student

✓ Detail Student

✓ Student By Class

✓ Search Student

Negative

✓ Invalid UUID

✓ Invalid Class UUID

✓ Empty Full Name

✓ Empty Photo

✓ Invalid Email

---

# 19. Performance

Pagination

Default

20 Data

Sorting

sort_order ASC

Index

uuid

class_id

sort_order

is_active

---

# 20. Future Improvement

- Favorite Student
- Student Achievement
- Student Organization
- Student Gallery
- Student Video
- Student PDF Profile
- QR Code Profile
- Import Excel
- Export Excel
