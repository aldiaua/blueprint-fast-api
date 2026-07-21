# Technical Requirement Document (TRD)

# 05. Principal Section

| Document     | Principal Section |
| ------------ | ----------------- |
| Version      | 1.0.0             |
| Status       | Draft             |
| Module       | Page Section      |
| Section Type | principal         |

---

# 1. Overview

Principal Section merupakan section yang menampilkan sambutan Kepala Sekolah kepada seluruh pengunjung website.

Section ini bersifat dinamis dan dapat diubah melalui CMS.

Data disimpan pada tabel:

page_sections

section_type

principal

---

# 2. UI Analysis

Berdasarkan HTML, section terdiri dari beberapa komponen berikut.

Principal Section

├── Section Badge

├── Section Title

├── Principal Photo

├── Principal Name

├── Principal Position

├── Greeting Content

├── Signature

└── Background Decoration

---

# 3. UI Breakdown

## Section Header

Komponen

- Badge
- Title

Dynamic

YES

---

## Principal Information

Komponen

- Photo
- Name
- Position

Dynamic

YES

---

## Greeting

Komponen

- Greeting Text

Dynamic

YES

---

## Signature

Komponen

- Signature Name
- Signature Position

Dynamic

YES

---

## Decoration

Komponen

- Background Ornament
- Shape
- Accent

Dynamic

YES

---

# 4. Database

Menggunakan tabel

page_sections

section_type

principal

---

# 5. Components JSON

```json
{
    "badge": {
        "text": "Sambutan"
    },

    "title": {
        "text": "Sambutan Kepala Sekolah"
    },

    "principal": {
        "name": "Drs. Ahmad Wijaya",
        "position": "Kepala Sekolah",
        "photo": "/assets/images/principal.jpg"
    },

    "greeting": {
        "content": "<p>...</p>"
    },

    "signature": {
        "name": "Drs. Ahmad Wijaya",
        "position": "Kepala Sekolah"
    }
}
```

---

# 6. Styles JSON

```json
{
    "background": {
        "color": "#FFFFFF"
    },

    "container": "container",

    "text": {
        "align": "left"
    },

    "spacing": {
        "padding_top": 120,
        "padding_bottom": 120
    },

    "animation": {
        "type": "fade-up"
    }
}
```

---

# 7. CMS Form

Administrator dapat mengubah:

## Section

- Badge
- Title

---

## Principal

- Name
- Position
- Photo

---

## Greeting

- Rich Text Editor

---

## Signature

- Name
- Position

---

## Style

- Background
- Padding
- Animation

---

# 8. Business Rules

- Badge opsional.
- Title wajib.
- Nama Kepala Sekolah wajib.
- Jabatan wajib.
- Greeting wajib.
- Photo opsional.
- Signature mengikuti data principal, tetapi dapat diubah jika diperlukan.

---

# 9. Public API

GET

/api/v1/page-sections/principal

Response

```json
{
    "success": true,
    "message": "Success",
    "data": {
        "section_type": "principal",
        "components": {},
        "styles": {}
    }
}
```

---

# 10. CMS API

GET

/api/v1/cms/page-sections/principal

PUT

/api/v1/cms/page-sections/principal

---

# 11. Validation

| Field              | Rule     |
| ------------------ | -------- |
| title              | Required |
| principal.name     | Required |
| principal.position | Required |
| greeting.content   | Required |
| photo              | Optional |
| badge              | Optional |

---

# 12. Repository

PageSectionRepository

Method

- getPrincipal()
- updatePrincipal()

---

# 13. Service

PageSectionService

Method

- getPrincipal()
- updatePrincipal()

---

# 14. Schema

PrincipalResponse

PrincipalUpdateRequest

---

# 15. Seeder

Seeder mengikuti HTML secara penuh.

Data yang disalin:

- Badge
- Title
- Nama Kepala Sekolah
- Jabatan
- Foto
- Isi Sambutan
- Signature
- Background

Tidak boleh mengubah isi sambutan ataupun asset bawaan template.

---

# 16. Testing

Positive

✓ Get Principal

✓ Update Greeting

✓ Update Photo

✓ Update Style

Negative

✓ Empty Title

✓ Empty Greeting

✓ Invalid JSON

✓ Invalid Image Path

---

# 17. Performance

Mengambil satu record pada tabel page_sections.

Target Response

< 50 ms

---

# 18. Future Improvement

- Video Greeting
- Digital Signature
- Audio Greeting
- Multiple Language
- Markdown Editor
- AI Grammar Check
