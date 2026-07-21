# Technical Requirement Document (TRD)

# 04. Cover Section

| Document     | Cover Section |
| ------------ | ------------- |
| Version      | 1.0.0         |
| Status       | Draft         |
| Module       | Page Section  |
| Section Type | cover         |

---

# 1. Overview

Cover merupakan section pertama yang ditampilkan ketika Website dibuka.

Section ini menjadi Hero Banner yang berfungsi memberikan identitas sekolah dan navigasi awal kepada pengunjung.

Section ini bersifat Dynamic dan seluruh datanya disimpan pada tabel page_sections dengan section_type = "cover".

---

# 2. UI Analysis

Berdasarkan HTML Template, Cover terdiri dari beberapa komponen utama.

```

Cover

├── Background

├── Overlay

├── School Logo

├── School Name

├── Academic Year

├── Headline

├── Description

├── Primary Button

├── Secondary Button

├── Statistics

└── Scroll Indicator

```

---

# 3. UI Breakdown

## 3.1 Background

Komponen:

- Background Image

- Background Overlay

- Overlay Opacity

- Background Position

Dynamic

YES

---

## 3.2 Logo

Komponen

- Logo Image

- Alt Text

Dynamic

YES

---

## 3.3 School Information

Komponen

- School Name

- Academic Year

- Tagline

Dynamic

YES

---

## 3.4 Hero Text

Komponen

- Heading

- Description

Dynamic

YES

---

## 3.5 CTA

Komponen

Primary Button

Secondary Button

Dynamic

YES

---

## 3.6 Statistics

Komponen

Statistic Card

Isi

- Total Teacher

- Total Student

- Total Class

Nilai statistic dapat diambil dari database ataupun manual.

---

## 3.7 Scroll Indicator

Komponen

Icon

Target Anchor

Dynamic

YES

---

# 4. Database

Tidak memiliki tabel sendiri.

Menggunakan

page_sections

section_type

cover

---

# 5. Components JSON

```json
{
    "school": {
        "name": "SMAN 1 Example",
        "academic_year": "2025/2026",
        "tagline": "Creating Future Leaders",
        "logo": {
            "url": "/assets/logo.png",
            "alt": "School Logo"
        }
    },

    "hero": {
        "title": "Memoria Yearbook",
        "description": "Every story deserves to be remembered."
    },

    "buttons": [
        {
            "label": "Lihat Guru",
            "url": "#teachers",
            "target": "_self"
        },
        {
            "label": "Lihat Galeri",
            "url": "#gallery",
            "target": "_self"
        }
    ],

    "statistics": [
        {
            "title": "Guru",
            "value": 50
        },
        {
            "title": "Siswa",
            "value": 1200
        },
        {
            "title": "Kelas",
            "value": 30
        }
    ],

    "scroll_indicator": {
        "enabled": true,
        "target": "#principal"
    }
}
```

---

# 6. Styles JSON

```json
{
    "background": {
        "image": "/assets/images/hero.jpg",
        "overlay": "#000000",
        "opacity": 0.45,
        "position": "center center",
        "size": "cover"
    },

    "container": {
        "width": "container"
    },

    "spacing": {
        "padding_top": 120,
        "padding_bottom": 120
    },

    "text": {
        "align": "center",
        "color": "#FFFFFF"
    },

    "animation": {
        "enabled": true,
        "type": "fade-up"
    }
}
```

---

# 7. CMS Form

Administrator dapat mengubah:

## School

- School Name
- Academic Year
- Tagline
- Logo

---

## Hero

- Title
- Description

---

## Button

- Label
- URL
- Target

---

## Statistic

- Title
- Value

---

## Background

- Background Image
- Overlay Color
- Overlay Opacity

---

# 8. Business Rules

- Minimal memiliki satu tombol.
- Maksimal dua tombol.
- Maksimal tiga statistic card.
- Background wajib tersedia.
- School Name wajib diisi.
- Hero Title wajib diisi.
- Logo bersifat opsional.

---

# 9. Public API

## GET

/api/v1/page-sections/cover

Response

```json
{
    "success": true,
    "message": "Success",
    "data": {
        "section_type": "cover",
        "components": {},
        "styles": {}
    }
}
```

---

# 10. CMS API

GET

/api/v1/cms/page-sections/cover

PUT

/api/v1/cms/page-sections/cover

---

# 11. Validation

School Name

Required

Hero Title

Required

Description

Required

Statistic

0-3 item

Button

1-2 item

Overlay

0-1

Opacity

0.0 - 1.0

---

# 12. Repository

PageSectionRepository

Method

findCover()

updateCover()

---

# 13. Service

PageSectionService

Method

getCover()

updateCover()

---

# 14. Schema

CoverResponse

CoverUpdateRequest

---

# 15. Seeder

Seeder akan diambil dari template HTML.

Seluruh data berikut akan dibuat sama persis:

- Background Image
- School Logo
- School Name
- Academic Year
- Hero Title
- Hero Description
- CTA Button
- Statistic
- Scroll Target

Tidak boleh ada perubahan asset.

---

# 16. Testing

Positive

✓ Get Cover

✓ Update Hero

✓ Update Background

✓ Update Button

✓ Update Statistic

Negative

✓ Empty School Name

✓ Empty Hero Title

✓ Invalid JSON

✓ Invalid Opacity

✓ More than 2 Buttons

✓ More than 3 Statistics

---

# 17. Performance

Endpoint ini dipanggil satu kali saat halaman pertama dibuka.

Karena hanya mengambil satu baris pada tabel page_sections, response time yang ditargetkan adalah kurang dari 50 ms pada kondisi normal.

---

# 18. Future Improvement

- Video Background
- Parallax Background
- Animated Counter
- Typing Animation
- Countdown
- Dynamic Theme
- Gradient Overlay
- Multi Language Hero
