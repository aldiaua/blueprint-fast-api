# Technical Requirement Document (TRD)

# 02. Settings Module

| Document | Settings |
|----------|----------|
| Version | 1.0.0 |
| Status | Draft |
| Module | CMS |

---

# 1. Overview

Settings merupakan module yang digunakan untuk menyimpan konfigurasi global website.

Berbeda dengan page_sections yang menyimpan konten halaman, settings menyimpan konfigurasi website yang digunakan di seluruh halaman.

Module ini menggunakan PostgreSQL JSONB agar konfigurasi dapat berkembang tanpa perubahan struktur database.

---

# 2. Objectives

Module Settings bertujuan untuk:

- Mengelola informasi website
- Mengelola Header
- Mengelola Footer
- Mengelola Theme
- Mengelola SEO
- Mengelola Social Media

Tanpa perlu membuat tabel baru.

---

# 3. Business Rules

- Setting harus memiliki setting_key yang unik.
- Setting menggunakan JSONB.
- Setting hanya boleh diakses oleh Administrator.
- Public API hanya dapat membaca data.
- setting_key menggunakan enum.
- Tidak diperbolehkan membuat setting_key baru melalui CMS.

---

# 4. Setting Key

| Key | Description |
|------|-------------|
| website | Website Information |
| header | Header Configuration |
| footer | Footer Configuration |
| seo | SEO Configuration |
| social | Social Media |
| theme | Theme Configuration |

---

# 5. Database Design

Table

settings

| Column | Type | Nullable | Description |
|---------|------|----------|-------------|
| id | BIGSERIAL | NO | Primary Key |
| setting_key | VARCHAR(50) | NO | Enum Key |
| components | JSONB | NO | Website Content |
| styles | JSONB | NO | UI Configuration |
| description | TEXT | YES | Description |
| created_at | TIMESTAMP | NO | Created Time |
| updated_at | TIMESTAMP | NO | Updated Time |

---

# 6. Index

PRIMARY KEY(id)

UNIQUE(setting_key)

---

# 7. Enum

website

header

footer

seo

social

theme

---

# 8. API

## Public

GET /api/v1/settings

GET /api/v1/settings/{setting_key}

---

## CMS

GET /api/v1/cms/settings

GET /api/v1/cms/settings/{setting_key}

PUT /api/v1/cms/settings/{setting_key}

---

# 9. Public Response

{
    "success": true,
    "message": "Success",
    "data": [
        {
            "setting_key": "header",
            "components": {},
            "styles": {}
        }
    ]
}

---

# 10. CMS Update Request

{
    "components": {

    },

    "styles": {

    }
}

---

# 11. Components Guideline

Components digunakan untuk menyimpan data.

Contoh:

{
    "logo": {
        "url": "",
        "alt": ""
    },

    "menus": [

    ],

    "buttons": [

    ]
}

---

# 12. Styles Guideline

Styles digunakan untuk tampilan.

{
    "background": {

    },

    "text": {

    },

    "spacing": {

    },

    "animation": {

    }
}

---

# 13. Header Components

Header menggunakan komponen berikut.

logo

menus

primary_button

secondary_button

announcement

---

# 14. Footer Components

Footer menggunakan komponen berikut.

logo

description

quick_links

social_links

copyright

contact

---

# 15. Website Components

Website

{
    "school_name": "",

    "tagline": "",

    "academic_year": "",

    "favicon": "",

    "logo": ""
}

---

# 16. SEO Components

{
    "title": "",

    "description": "",

    "keywords": [],

    "author": "",

    "robots": "index,follow",

    "og_image": ""
}

---

# 17. Theme Components

{
    "primary_color": "#2563EB",

    "secondary_color": "#111827",

    "font_family": "Inter",

    "border_radius": "8",

    "container": "xl"
}

---

# 18. Social Components

{
    "instagram": "",

    "facebook": "",

    "youtube": "",

    "tiktok": "",

    "linkedin": ""
}

---

# 19. Validation

- setting_key wajib valid.
- components wajib JSON Object.
- styles wajib JSON Object.
- Tidak boleh NULL.
- JSON harus valid.

---

# 20. Repository

SettingsRepository

Method

- find_all()

- find_by_key()

- update()

---

# 21. Service

SettingsService

Method

- get_all()

- get_by_key()

- update()

---

# 22. Schema

SettingsResponse

SettingsUpdateRequest

SettingsListResponse

---

# 23. Migration

CREATE TABLE settings (

id BIGSERIAL PRIMARY KEY,

setting_key VARCHAR(50) UNIQUE NOT NULL,

components JSONB NOT NULL,

styles JSONB NOT NULL,

description TEXT,

created_at TIMESTAMP NOT NULL,

updated_at TIMESTAMP NOT NULL

);

---

# 24. Seeder

## website

{
    "school_name": "",
    "tagline": "",
    "academic_year": ""
}

---

## header

{
    "logo": {},
    "menus": [],
    "primary_button": {},
    "secondary_button": {}
}

---

## footer

{
    "description": "",
    "quick_links": [],
    "social_links": [],
    "copyright": ""
}

---

## seo

{
    "title": "",
    "description": "",
    "keywords": []
}

---

## social

{
    "instagram": "",
    "facebook": "",
    "youtube": ""
}

---

## theme

{
    "primary_color": "#2563EB",
    "secondary_color": "#111827"
}

---

# 25. Testing

Positive

✓ Get Setting

✓ Update Setting

✓ Update Header

✓ Update Footer

✓ Update Theme

Negative

✓ Invalid JSON

✓ Invalid Enum

✓ Empty Components

✓ Empty Styles

✓ Unknown Setting Key
