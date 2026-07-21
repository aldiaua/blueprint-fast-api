# Technical Requirement Document (TRD)

# 01. Database Design

| Document | Database Design |
| -------- | --------------- |
| Version  | 1.0.0           |
| Status   | Draft           |
| Database | PostgreSQL      |
| Engine   | PostgreSQL 16+  |

---

# 1. Overview

Dokumen ini menjelaskan desain database yang digunakan oleh Yearbook CMS API.

Database dirancang berdasarkan prinsip:

- Simple
- Readable
- Easy Maintenance
- JSONB for Dynamic Content
- Normalized for Master Data

Target utama adalah mengurangi kompleksitas tanpa mengurangi fleksibilitas.

---

# 2. Database Philosophy

Database dibagi menjadi dua jenis data.

## Dynamic Data

Data yang sering berubah bentuk.

Contoh:

- Header
- Footer
- Cover
- Principal Greeting
- Gallery Layout
- Theme
- Website Setting

Dynamic Data menggunakan PostgreSQL JSONB.

---

## Master Data

Data yang mempunyai struktur tetap.

Contoh

Teacher

Student

Class

Student Group

Master Data menggunakan Relational Table.

---

# 3. Database Diagram

                     settings

                         │

                         │

                         ▼

                  page_sections

                         │

     ┌──────────────┬─────────────┐

     ▼              ▼             ▼

teachers classes student_groups

                                    │

                                    ▼

                                students

---

# 4. Table Overview

| Table          | Purpose               |
| -------------- | --------------------- |
| settings       | Website Configuration |
| page_sections  | Dynamic Section       |
| teachers       | Master Teacher        |
| classes        | Master Class          |
| student_groups | Student Group         |
| students       | Student Master        |

Total hanya enam tabel.

---

# 5. Table Detail

## settings

Digunakan untuk menyimpan konfigurasi website.

Contoh

- Website
- Header
- Footer
- Theme
- SEO
- Social Media

Tidak digunakan untuk data master.

---

## page_sections

Digunakan untuk menyimpan section yang bersifat dinamis.

Contoh

- Cover
- Principal Greeting
- Generation
- Gallery
- Quote
- Video
- Custom Section

Section diurutkan berdasarkan sort_order.

---

## teachers

Menyimpan seluruh data guru.

Tidak menggunakan JSONB.

Semua field menggunakan Relational Database.

---

## classes

Master seluruh kelas.

Contoh

X IPA 1

XI IPA 2

XII IPS 1

---

## student_groups

Grouping siswa.

Contoh

XII IPA 1

↓

Group A

Group B

Group C

---

## students

Master siswa.

Setiap siswa wajib memiliki:

- Class
- Group

---

# 6. Entity Relationship

teachers

↓

classes

↓

student_groups

↓

students

Sedangkan

settings

dan

page_sections

berdiri sendiri.

---

# 7. JSONB Standard

Semua JSONB memiliki dua object utama.

components

styles

Tidak diperbolehkan membuat struktur lain.

---

Contoh

{
"components":{

    },

    "styles":{

    }

}

---

# 8. JSON Component Guideline

Components digunakan untuk menyimpan seluruh data yang ditampilkan.

Contoh

{
"title":{

    },

    "subtitle":{

    },

    "buttons":[

    ],

    "gallery":[

    ]

}

---

# 9. JSON Style Guideline

Styles digunakan untuk tampilan.

Contoh

{
"background":{

    },

    "spacing":{

    },

    "animation":{

    }

}

---

# 10. UUID Policy

Semua tabel menggunakan UUID.

UUID digunakan sebagai Public Identifier.

Primary Key Integer digunakan untuk relasi internal.

---

# 11. Naming Convention

Table

snake_case

Field

snake_case

API

kebab-case

JSON

camelCase

---

# 12. Timestamp Standard

Semua tabel menggunakan

created_at

updated_at

Sedangkan tabel yang membutuhkan publish menggunakan

is_active

---

# 13. Soft Delete Policy

Project tidak menggunakan Soft Delete.

Data dihapus permanen.

Alasan:

- Database sederhana
- Tidak membutuhkan recycle bin
- Mengurangi kompleksitas query

Apabila di masa depan dibutuhkan Audit Log, maka akan dibuat tabel audit_logs terpisah.

---

# 14. Sort Order Policy

Seluruh data yang ditampilkan memiliki field

sort_order

Semakin kecil berarti semakin atas.

---

# 15. Index Standard

Semua tabel wajib memiliki:

PRIMARY KEY

UNIQUE(uuid)

INDEX(sort_order)

INDEX(is_active)

apabila field tersedia.

---

# 16. Constraint Standard

Teacher

Tidak boleh memiliki UUID yang sama.

Student

Harus mempunyai Class.

Student

Harus mempunyai Student Group.

Group

Harus mempunyai Class.

---

# 17. Storage Decision

Mengapa Header tidak dibuat tabel sendiri?

Karena Header bersifat Dynamic.

Menggunakan JSONB jauh lebih fleksibel.

---

Mengapa Cover tidak dibuat tabel?

Karena seluruh komponennya berubah-ubah.

Lebih cocok menggunakan JSONB.

---

Mengapa Teacher dibuat tabel?

Karena membutuhkan CRUD.

Pencarian.

Sorting.

Filtering.

---

Mengapa Student dibuat tabel?

Karena memiliki relasi.

Class.

Group.

Sorting.

Filtering.

---

# 18. Performance Consideration

Jumlah data diperkirakan

Teacher

<100

Student

<3000

Class

<100

Group

<500

Section

<30

Setting

<20

Sehingga PostgreSQL sangat mampu menangani seluruh query tanpa optimisasi khusus.

---

# 19. Future Expansion

Database memungkinkan penambahan:

- Alumni
- Event
- Achievement
- Organization
- Extracurricular
- Multiple Theme

tanpa mengubah tabel yang sudah ada.

---

# 20. Database Checklist

✓ Menggunakan PostgreSQL

✓ Menggunakan JSONB

✓ Hanya enam tabel utama

✓ Mudah dipahami

✓ Mudah dikembangkan

✓ Konsisten

✓ Mendukung REST API

✓ Mendukung CMS

✓ Mendukung Dynamic Content

✓ Siap digunakan pada Production
