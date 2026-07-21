# Technical Requirement Document (TRD)

# 03. Page Sections

| Document | Page Sections |
| -------- | ------------- |
| Version  | 1.0.0         |
| Status   | Draft         |
| Module   | CMS           |

---

# 1. Overview

Page Sections merupakan module yang bertanggung jawab mengelola seluruh konten dinamis yang ditampilkan pada halaman utama Website Yearbook.

Section merupakan kumpulan komponen yang ditampilkan secara berurutan dari atas ke bawah.

Contoh:

Header

↓

Cover

↓

Principal Greeting

↓

Teachers

↓

Generation

↓

Classes

↓

Gallery

↓

Footer

Seluruh section menggunakan struktur JSONB agar dapat berubah tanpa perubahan struktur database.

---

# 2. Objectives

Module ini bertujuan untuk:

- Mengelola seluruh konten landing page
- Mengatur urutan section
- Mengatur publish/unpublish section
- Mengubah tampilan section
- Menyediakan data untuk Public API

---

# 3. Section Type

Berikut section yang ditemukan dari template HTML.

| Section Type | Dynamic |
| ------------ | ------- |
| cover        | ✔       |
| principal    | ✔       |
| teachers     | ✔       |
| generation   | ✔       |
| classes      | ✔       |
| gallery      | ✔       |

Header dan Footer dikelola melalui module Settings.

---

# 4. UI Breakdown

Website

```
Header

↓

Cover

↓

Principal Greeting

↓

Teachers

↓

Generation

↓

Classes

↓

Gallery

↓

Footer
```

Render dilakukan berdasarkan sort_order.

---

# 5. Database

Table

page_sections

| Column       | Type         | Nullable | Description          |
| ------------ | ------------ | -------- | -------------------- |
| id           | BIGSERIAL    | NO       | Primary Key          |
| uuid         | UUID         | NO       | Public UUID          |
| section_type | VARCHAR(50)  | NO       | Jenis Section        |
| title        | VARCHAR(255) | NO       | Nama Section di CMS  |
| components   | JSONB        | NO       | Konten               |
| styles       | JSONB        | NO       | Konfigurasi Tampilan |
| sort_order   | INTEGER      | NO       | Urutan Tampil        |
| is_active    | BOOLEAN      | NO       | Publish Status       |
| created_at   | TIMESTAMP    | NO       | Created Time         |
| updated_at   | TIMESTAMP    | NO       | Updated Time         |

---

# 6. Allowed Section Type

cover

principal

teachers

generation

classes

gallery

---

# 7. Components JSON

Field components digunakan untuk menyimpan seluruh data yang akan dirender oleh Frontend.

Contoh struktur umum

```json
{
    "title": {},
    "subtitle": {},
    "description": {},
    "buttons": [],
    "items": [],
    "statistics": []
}
```

Setiap section memiliki struktur components yang berbeda sesuai kebutuhannya.

---

# 8. Styles JSON

Styles hanya menyimpan konfigurasi tampilan.

```json
{
    "background": {
        "color": "#FFFFFF",
        "image": ""
    },
    "spacing": {
        "top": 100,
        "bottom": 100
    },
    "container": "container",
    "animation": "fade-up"
}
```

Styles tidak boleh menyimpan data bisnis.

---

# 9. Business Rules

- Section Type harus unik.
- Section dapat diaktifkan atau dinonaktifkan.
- Sort Order harus unik.
- Components wajib berupa JSON Object.
- Styles wajib berupa JSON Object.
- Public API hanya menampilkan section aktif.

---

# 10. Public API

## List Section

GET

/api/v1/page-sections

Response

```json
{
    "success": true,
    "message": "Success",
    "data": [
        {
            "section_type": "cover",
            "title": "Cover",
            "components": {},
            "styles": {}
        }
    ]
}
```

---

## Detail Section

GET

/api/v1/page-sections/{section_type}

---

# 11. CMS API

## List

GET

/api/v1/cms/page-sections

---

## Detail

GET

/api/v1/cms/page-sections/{section_type}

---

## Update

PUT

/api/v1/cms/page-sections/{section_type}

---

# 12. Update Request

```json
{
    "components": {},
    "styles": {}
}
```

---

# 13. Validation

- section_type wajib valid.
- components wajib JSON.
- styles wajib JSON.
- title tidak boleh kosong.
- sort_order harus lebih besar dari 0.
- section_type tidak boleh diubah setelah dibuat.

---

# 14. Repository

PageSectionRepository

Method

- findAll()
- findActive()
- findByType()
- update()

---

# 15. Service

PageSectionService

Method

- getSections()
- getSection()
- updateSection()

---

# 16. Schema

PageSectionResponse

PageSectionListResponse

PageSectionUpdateRequest

---

# 17. Migration

```sql
CREATE TABLE page_sections (

id BIGSERIAL PRIMARY KEY,

uuid UUID NOT NULL UNIQUE,

section_type VARCHAR(50) NOT NULL UNIQUE,

title VARCHAR(255) NOT NULL,

components JSONB NOT NULL,

styles JSONB NOT NULL,

sort_order INTEGER NOT NULL,

is_active BOOLEAN DEFAULT TRUE,

created_at TIMESTAMP NOT NULL,

updated_at TIMESTAMP NOT NULL

);
```

---

# 18. Seeder

Seeder akan dibuat berdasarkan template HTML.

Data awal:

| Sort | Section    |
| ---- | ---------- |
| 1    | cover      |
| 2    | principal  |
| 3    | teachers   |
| 4    | generation |
| 5    | classes    |
| 6    | gallery    |

Field components akan diisi sesuai isi HTML.

Field styles akan mengikuti style bawaan template HTML.

---

# 19. Testing

Positive

✓ Get All Section

✓ Get Detail Section

✓ Update Section

✓ Publish Section

✓ Unpublish Section

Negative

✓ Invalid Section Type

✓ Invalid JSON

✓ Duplicate Sort Order

✓ Empty Components

✓ Empty Styles

---

# 20. Future Improvement

- Duplicate Section
- Drag & Drop Sorting
- Section Versioning
- Schedule Publish
- Draft Mode
- Import / Export JSON
