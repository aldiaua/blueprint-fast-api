# Technical Requirement Document (TRD)

# 10. Public API

| Document | Public API      |
| -------- | --------------- |
| Version  | 1.0.0           |
| Status   | Draft           |
| API Type | Public REST API |

---

# 1. Overview

Public API digunakan oleh Frontend Website.

Seluruh endpoint bersifat Read Only.

Authentication tidak diperlukan.

Semua endpoint hanya menampilkan data dengan:

is_active = TRUE

---

# 2. API List

| Method | Endpoint                        | Description       |
| ------ | ------------------------------- | ----------------- |
| GET    | /api/v1/landing                 | Landing Page      |
| GET    | /api/v1/settings                | Website Settings  |
| GET    | /api/v1/teachers                | Teacher List      |
| GET    | /api/v1/teachers/{uuid}         | Teacher Detail    |
| GET    | /api/v1/classes                 | Class List        |
| GET    | /api/v1/classes/{uuid}          | Class Detail      |
| GET    | /api/v1/classes/{uuid}/students | Students By Class |
| GET    | /api/v1/students                | Student List      |
| GET    | /api/v1/students/{uuid}         | Student Detail    |

---

# 3. Landing API

GET

/api/v1/landing

Endpoint ini merupakan endpoint utama website.

Frontend hanya perlu memanggil satu endpoint ketika halaman pertama dibuka.

---

# 4. Landing Response

```json
{
    "success": true,
    "message": "Success",
    "data": {
        "settings": {},
        "sections": {
            "cover": {},
            "principal": {},
            "generation": {}
        },
        "teachers": [],
        "classes": []
    }
}
```

---

# 5. Data Source

Landing API mengambil data dari:

settings

↓

page_sections

↓

teachers

↓

classes

Tidak mengambil students untuk mengurangi payload.

---

# 6. Teacher List

GET

/api/v1/teachers

Query

page

limit

search

---

# 7. Teacher Detail

GET

/api/v1/teachers/{uuid}

---

# 8. Class List

GET

/api/v1/classes

Query

page

limit

search

year

---

# 9. Class Detail

GET

/api/v1/classes/{uuid}

---

# 10. Student By Class

GET

/api/v1/classes/{uuid}/students

---

# 11. Student List

GET

/api/v1/students

Query

page

limit

search

class_uuid

---

# 12. Student Detail

GET

/api/v1/students/{uuid}

---

# 13. Standard Response

Success

```json
{
    "success": true,
    "message": "Success",
    "data": {}
}
```

---

Error

```json
{
    "success": false,
    "message": "Validation Error",
    "errors": []
}
```

---

# 14. Pagination

```json
{
    "meta": {
        "page": 1,
        "limit": 20,
        "total": 120,
        "last_page": 6
    }
}
```

---

# 15. Sorting

Default

sort_order ASC

---

# 16. Search

Search dilakukan menggunakan

ILIKE

pada PostgreSQL.

---

# 17. Performance

Landing API

Target

< 100 ms

Teacher List

< 50 ms

Class List

< 50 ms

Student List

< 100 ms

---

# 18. Cache Strategy

Endpoint yang dapat di-cache:

- /landing
- /settings
- /teachers
- /classes

TTL

300 detik

Endpoint Student tidak disarankan menggunakan cache karena lebih sering berubah.

---

# 19. Security

Public API

Tidak membutuhkan JWT.

Rate Limit

60 request / menit / IP.

---

# 20. Future Improvement

- GraphQL Endpoint
- ETag Support
- HTTP Cache
- CDN Cache
- Incremental Static Regeneration
