# Technical Requirement Document (TRD)

# 07. Generation Section

| Document     | Generation Section |
| ------------ | ------------------ |
| Version      | 1.0.0              |
| Status       | Draft              |
| Module       | Page Section       |
| Section Type | generation         |

---

# 1. Overview

Generation Section digunakan untuk menampilkan informasi angkatan yang sedang dibuat pada website Yearbook.

Section ini berisi informasi umum mengenai angkatan, motto, jumlah siswa, jumlah kelas, tahun kelulusan, serta narasi singkat.

Section ini merupakan Dynamic Section sehingga seluruh data disimpan pada tabel page_sections.

---

# 2. UI Analysis

Berdasarkan HTML Template, section terdiri dari:

Generation

├── Section Header

│ ├── Badge

│ ├── Title

│ └── Description

│

├── Generation Information

│ ├── Generation Name

│ ├── Graduation Year

│ ├── Motto

│ └── Narrative

│

└── Statistics

├── Total Students

├── Total Teachers

├── Total Classes

└── Graduation Year

---

# 3. Database

Table

page_sections

section_type

generation

---

# 4. Components

```json
{
    "header": {
        "badge": "Angkatan",
        "title": "Generasi 2025",
        "description": "Perjalanan kami dalam satu cerita."
    },

    "generation": {
        "name": "Generation Alpha",
        "graduation_year": "2025",
        "motto": "Together We Grow",
        "story": ""
    },

    "statistics": [
        {
            "label": "Guru",
            "value": 56
        },
        {
            "label": "Kelas",
            "value": 18
        },
        {
            "label": "Siswa",
            "value": 612
        }
    ]
}
```

---

# 5. Styles

```json
{
    "background": {
        "color": "#FFFFFF",
        "image": ""
    },

    "spacing": {
        "top": 120,
        "bottom": 120
    },

    "container": "container",

    "animation": {
        "type": "fade-up"
    }
}
```

---

# 6. CMS Form

Section Header

- Badge
- Title
- Description

Generation

- Generation Name
- Graduation Year
- Motto
- Story

Statistics

- Label
- Value

Style

- Background
- Padding
- Animation

---

# 7. Business Rules

- Badge opsional.
- Title wajib.
- Generation Name wajib.
- Graduation Year wajib.
- Motto opsional.
- Story mendukung HTML.
- Maksimal empat statistic card.

---

# 8. Public API

GET

/api/v1/page-sections/generation

---

# 9. CMS API

GET

/api/v1/cms/page-sections/generation

PUT

/api/v1/cms/page-sections/generation

---

# 10. Validation

Header Title

Required

Generation Name

Required

Graduation Year

Required

Story

Optional

Statistics

Maximum 4 items

---

# 11. Repository

PageSectionRepository

Method

findGeneration()

updateGeneration()

---

# 12. Service

PageSectionService

Method

getGeneration()

updateGeneration()

---

# 13. Schema

GenerationResponse

GenerationUpdateRequest

---

# 14. Seeder

Mengikuti isi HTML.

Data berikut harus sama persis:

- Badge
- Title
- Description
- Generation Name
- Motto
- Graduation Year
- Story
- Statistic

---

# 15. Testing

Positive

✓ Get Generation

✓ Update Motto

✓ Update Story

✓ Update Statistic

Negative

✓ Empty Title

✓ Empty Generation Name

✓ Empty Graduation Year

✓ Invalid JSON

✓ Statistic lebih dari 4

---

# 16. Performance

Hanya mengambil satu record pada tabel page_sections.

Target response

< 50 ms

---

# 17. Future Improvement

- Timeline Angkatan
- Video Angkatan
- Spotify Playlist
- Achievement
- Organization
- Event Highlight
- Alumni Message
