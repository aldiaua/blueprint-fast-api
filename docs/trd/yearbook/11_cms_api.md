# Technical Requirement Document (TRD)

# 11. CMS API

| Document       | CMS API |
| -------------- | ------- |
| Version        | 1.0.0   |
| Status         | Draft   |
| Authentication | JWT     |

---

# 1. Overview

CMS API digunakan oleh Administrator untuk mengelola seluruh data website.

Semua endpoint menggunakan JWT Authentication.

Base URL

/api/v1/cms

---

# 2. API Modules

| Module        | Endpoint       |
| ------------- | -------------- |
| Settings      | /settings      |
| Page Sections | /page-sections |
| Teachers      | /teachers      |
| Classes       | /classes       |
| Students      | /students      |

---

# 3. Authentication

Authorization

Bearer Token

```
Authorization: Bearer xxxxxxxxx
```

---

# 4. Settings

## List

GET

/api/v1/cms/settings

---

## Detail

GET

/api/v1/cms/settings/{setting_key}

---

## Update

PUT

/api/v1/cms/settings/{setting_key}

---

# 5. Page Sections

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

# 6. Teachers

## List

GET

/api/v1/cms/teachers

Query

page

limit

search

sort

order

---

## Detail

GET

/api/v1/cms/teachers/{uuid}

---

## Create

POST

/api/v1/cms/teachers

---

## Update

PUT

/api/v1/cms/teachers/{uuid}

---

## Delete

DELETE

/api/v1/cms/teachers/{uuid}

---

# 7. Classes

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

# 8. Students

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

# 9. Common Query Parameter

page

Default

1

---

limit

Default

20

Maximum

100

---

search

String

---

sort

Column Name

---

order

asc

desc

---

is_active

true

false

---

# 10. Standard Response

Success

```json
{
    "success": true,
    "message": "Success",
    "data": {}
}
```

Validation Error

```json
{
    "success": false,
    "message": "Validation Error",
    "errors": [
        {
            "field": "name",
            "message": "Name is required."
        }
    ]
}
```

---

# 11. HTTP Status

200 OK

201 Created

204 No Content

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Validation Error

500 Internal Server Error

---

# 12. Filtering Standard

Teachers

search

position

subject

is_active

---

Classes

search

graduation_year

is_active

---

Students

search

class_uuid

gender

is_active

---

# 13. Sorting Standard

Default

sort_order ASC

Alternative

created_at DESC

updated_at DESC

name ASC

---

# 14. Bulk Operation

Future Endpoint

POST

/bulk-delete

POST

/import

GET

/export

---

# 15. Upload Strategy

Upload dilakukan melalui endpoint Media.

Response

```json
{
    "uuid": "media_uuid",
    "url": "https://cdn.example.com/uploads/logo.png"
}
```

Endpoint lain hanya menerima:

media_uuid

---

# 16. Validation

Semua Request menggunakan

Pydantic Schema

Tidak boleh menerima field yang tidak terdaftar.

---

# 17. Logging

Semua endpoint mencatat:

Request ID

User UUID

Execution Time

Endpoint

HTTP Method

IP Address

Status Code

---

# 18. Audit Trail (Future)

Activity Log

Create

Update

Delete

Login

Logout

Export

Import

---

# 19. Security

JWT Authentication

Permission Middleware

Rate Limit

Input Validation

SQL Injection Protection

XSS Protection

---

# 20. Performance

Pagination wajib.

Search menggunakan Index.

Tidak boleh SELECT *.

Semua query menggunakan Repository Layer.

---

# 21. API Checklist

✓ RESTful

✓ Pagination

✓ Filtering

✓ Searching

✓ Sorting

✓ Validation

✓ Authentication

✓ Standard Response

✓ UUID Public Identifier

✓ Repository Pattern

✓ Service Layer
