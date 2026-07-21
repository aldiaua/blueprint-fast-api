# Technical Requirement Document (TRD)

# 08. Classes Module

| Document | Classes     |
| -------- | ----------- |
| Version  | 1.0.0       |
| Status   | Draft       |
| Module   | Master Data |

---

# 1. Overview

Classes merupakan Master Data yang digunakan untuk menyimpan seluruh informasi kelas pada Yearbook.

Data kelas digunakan oleh:

- Landing Page
- Detail Kelas
- Student Module
- Gallery (Opsional)
- Public API
- CMS

Classes bukan Dynamic Content sehingga menggunakan tabel Relational.

---

# 2. Objectives

Module ini bertujuan untuk:

- CRUD Kelas
- Mengatur urutan kelas
- Mengelompokkan siswa
- Menampilkan informasi kelas
- Menjadi parent dari Student

---

# 3. UI Analysis

Berdasarkan HTML, setiap kelas memiliki informasi:

```
Class Card

├── Cover Image
├── Class Name
├── Description
├── Homeroom Teacher
├── Student Count
└── Detail Button
```

Saat tombol "Detail" dipilih, sistem akan menampilkan seluruh siswa pada kelas tersebut.

---

# 4. Database

Table

classes

| Column              | Type         | Nullable | Description       |
| ------------------- | ------------ | -------- | ----------------- |
| id                  | BIGSERIAL    | NO       | Primary Key       |
| uuid                | UUID         | NO       | Public Identifier |
| name                | VARCHAR(100) | NO       | Nama Kelas        |
| slug                | VARCHAR(120) | NO       | URL Slug          |
| description         | TEXT         | YES      | Deskripsi         |
| cover_image         | TEXT         | YES      | Foto Cover        |
| homeroom_teacher_id | BIGINT       | YES      | FK Teachers       |
| graduation_year     | SMALLINT     | NO       | Tahun Kelulusan   |
| sort_order          | INTEGER      | NO       | Urutan            |
| is_active           | BOOLEAN      | NO       | Publish           |
| created_at          | TIMESTAMP    | NO       | Created           |
| updated_at          | TIMESTAMP    | NO       | Updated           |

---

# 5. Relationship

teachers (1)

↓

classes

↓

student_groups

↓

students

---

# 6. Business Rules

- Nama kelas unik pada tahun kelulusan yang sama.
- Slug dibuat otomatis dari nama kelas.
- Cover image bersifat opsional.
- Homeroom Teacher opsional.
- Kelas yang memiliki siswa tidak dapat dihapus.
- Class wajib aktif agar muncul di Website.

---

# 7. Public API

## List Class

GET

/api/v1/classes

Query

page

limit

search

year

---

## Detail

GET

/api/v1/classes/{uuid}

---

## Students

GET

/api/v1/classes/{uuid}/students

---

# 8. CMS API

GET

/api/v1/cms/classes

GET

/api/v1/cms/classes/{uuid}

POST

/api/v1/cms/classes

PUT

/api/v1/cms/classes/{uuid}

DELETE

/api/v1/cms/classes/{uuid}

---

# 9. Create Request

```json
{
    "name": "XII IPA 1",
    "description": "",
    "cover_image": "",
    "homeroom_teacher_uuid": "",
    "graduation_year": 2025,
    "sort_order": 1,
    "is_active": true
}
```

---

# 10. Response

```json
{
    "success": true,
    "message": "Success",
    "data": {
        "uuid": "",
        "name": "XII IPA 1",
        "slug": "xii-ipa-1"
    }
}
```

---

# 11. Validation

| Field                 | Rule     |
| --------------------- | -------- |
| name                  | Required |
| graduation_year       | Required |
| sort_order            | Required |
| homeroom_teacher_uuid | Optional |
| description           | Optional |
| cover_image           | Optional |
| is_active             | Boolean  |

---

# 12. Repository

ClassRepository

Method

- findAll()
- findByUUID()
- create()
- update()
- delete()
- getStudents()

---

# 13. Service

ClassService

Method

- getClasses()
- getClass()
- createClass()
- updateClass()
- deleteClass()
- getStudents()

---

# 14. Schema

ClassCreateRequest

ClassUpdateRequest

ClassResponse

ClassListResponse

---

# 15. Migration

```sql
CREATE TABLE classes (

id BIGSERIAL PRIMARY KEY,

uuid UUID NOT NULL UNIQUE,

name VARCHAR(100) NOT NULL,

slug VARCHAR(120) NOT NULL UNIQUE,

description TEXT,

cover_image TEXT,

homeroom_teacher_id BIGINT REFERENCES teachers(id),

graduation_year SMALLINT NOT NULL,

sort_order INTEGER NOT NULL,

is_active BOOLEAN DEFAULT TRUE,

created_at TIMESTAMP NOT NULL,

updated_at TIMESTAMP NOT NULL

);
```

---

# 16. Seeder

Seeder mengikuti HTML.

Data yang disalin:

- Nama Kelas
- Cover Image
- Deskripsi
- Wali Kelas
- Sort Order

Asset menggunakan file yang sama dengan template HTML.

---

# 17. Testing

Positive

✓ Create Class

✓ Update Class

✓ Delete Empty Class

✓ List Class

✓ Detail Class

✓ Get Students

Negative

✓ Duplicate Class Name

✓ Invalid Teacher UUID

✓ Invalid UUID

✓ Delete Class With Students

✓ Empty Class Name

---

# 18. Performance

Default Sorting

sort_order ASC

Pagination

20 Data

Target Response

< 100 ms

---

# 19. Future Improvement

- QR Code Kelas
- Class Achievement
- Class Playlist
- Class Video
- Class Timeline
- Download Class PDF
- Export Excel
