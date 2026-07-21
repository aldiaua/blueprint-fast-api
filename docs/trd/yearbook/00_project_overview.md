# Technical Requirement Document (TRD)

# 00. Project Overview

| Document | Yearbook CMS API |
|----------|------------------|
| Version | 1.0.0 |
| Status | Draft |
| Project | Yearbook Digital Platform |
| Architecture | REST API |
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migration | Alembic |

---

# 1. Overview

Yearbook CMS API merupakan Backend Service yang bertugas menyediakan seluruh data yang dibutuhkan Website Yearbook.

Backend dibangun menggunakan FastAPI dengan pendekatan RESTful API.

Seluruh konten Website bersifat dinamis dan dapat dikelola melalui CMS tanpa melakukan perubahan pada source code Frontend.

Backend dirancang menggunakan Repository Pattern, Service Layer, Schema Validation, serta PostgreSQL JSONB agar mudah dikembangkan.

---

# 2. Objectives

Tujuan utama project ini adalah:

- Menyediakan API Public untuk Website.
- Menyediakan API CMS untuk Administrator.
- Seluruh konten dapat dikelola melalui Dashboard.
- Struktur Database tetap sederhana.
- Mudah dikembangkan menjadi Template lain.
- Mudah di-maintain.
- Memiliki dokumentasi yang lengkap.

---

# 3. Scope

Project terdiri dari dua aplikasi.

## Public Website

Website yang dapat diakses seluruh pengunjung.

Contoh:

- Landing Page
- Cover
- Guru
- Kelas
- Siswa
- Gallery
- Footer

---

## CMS

Website Administrator.

Digunakan untuk:

- Login
- Mengubah Header
- Mengubah Footer
- Mengubah Cover
- CRUD Guru
- CRUD Kelas
- CRUD Group
- CRUD Siswa
- Mengatur Dynamic Section

---

# 4. Technology Stack

## Backend

FastAPI

---

## ORM

SQLAlchemy

---

## Migration

Alembic

---

## Database

PostgreSQL

---

## Validation

Pydantic

---

## Authentication

JWT

---

## API Documentation

Swagger OpenAPI

---

# 5. Project Structure

app

├── api

├── config

├── dependencies

├── middleware

├── repositories

├── services

├── schemas

├── models

├── responses

├── utils

---

Semua module mengikuti struktur tersebut.

---

# 6. Architecture

Presentation Layer

↓

API Router

↓

Service Layer

↓

Repository Layer

↓

Database

---

# 7. Database Overview

Project menggunakan enam tabel utama.

| Table | Description |
|--------|-------------|
| settings | Website Configuration |
| page_sections | Dynamic Website Section |
| teachers | Master Teacher |
| classes | Master Class |
| student_groups | Group Student |
| students | Master Student |

---

# 8. Database Philosophy

Project menggunakan kombinasi Relational Database dan JSONB.

## Relational Table

Digunakan untuk data yang sering dicari.

Contoh

- Teacher
- Student
- Class

---

## JSONB

Digunakan untuk data yang bersifat dinamis.

Contoh

- Header
- Footer
- Cover
- Principal Greeting
- Generation
- Gallery

---

# 9. Dynamic Content

Dynamic Content disimpan pada tabel:

page_sections

Field

components

styles

Dengan demikian Frontend cukup melakukan rendering berdasarkan data API.

---

# 10. Website Configuration

Konfigurasi Website disimpan pada tabel:

settings

Digunakan untuk:

- Website Information
- Header
- Footer
- Theme
- SEO
- Social Media

---

# 11. Master Data

Master Data dipisahkan agar mudah dilakukan CRUD.

## Teacher

Informasi seluruh Guru.

---

## Class

Informasi seluruh Kelas.

---

## Student Group

Grouping siswa.

---

## Student

Informasi seluruh siswa.

---

# 12. API Group

API dibagi menjadi dua kategori.

## Public API

Tidak membutuhkan Login.

Digunakan Frontend Website.

Contoh

GET /api/v1/settings

GET /api/v1/page-sections

GET /api/v1/teachers

GET /api/v1/classes

GET /api/v1/students

---

## CMS API

Membutuhkan Authentication.

Digunakan Administrator.

Contoh

GET

POST

PUT

DELETE

untuk seluruh Module.

---

# 13. Coding Standard

Seluruh Module wajib memiliki:

Repository

↓

Service

↓

Schema

↓

Router

↓

Response

Tidak diperbolehkan melakukan Query Database langsung dari Router.

---

# 14. API Response Standard

Seluruh API wajib menggunakan format berikut.

Success

{
    "success": true,
    "message": "Success",
    "data": {}
}

Error

{
    "success": false,
    "message": "Validation Error",
    "errors": []
}

---

# 15. UUID Policy

Seluruh API menggunakan UUID sebagai Public Identifier.

Primary Key Integer hanya digunakan untuk Relasi Internal.

Contoh

/api/v1/students/8b7bb44d-...

---

# 16. Sorting Policy

Seluruh data yang ditampilkan pada Website menggunakan field:

sort_order

Semakin kecil nilai maka semakin atas.

---

# 17. Publish Policy

Seluruh data Website menggunakan field

is_active

TRUE

Ditampilkan.

FALSE

Disembunyikan.

Tidak perlu menghapus data.

---

# 18. Security

Semua CMS API menggunakan JWT Authentication.

Semua endpoint wajib melakukan validasi Request.

Semua Input wajib melalui Schema Validation.

---

# 19. Error Handling

Seluruh Error menggunakan Standard Response.

400

Bad Request

401

Unauthorized

403

Forbidden

404

Not Found

409

Conflict

422

Validation Error

500

Internal Server Error

---

# 20. Logging

Seluruh Request dicatat oleh Middleware.

Informasi yang dicatat:

- Request ID
- Endpoint
- Execution Time
- Status Code
- Error Message

---

# 21. Future Roadmap

Versi berikutnya akan mendukung:

- Multi School
- Multi Theme
- Multi Language
- Multiple Yearbook
- Event Module
- Alumni Module
- Search Engine
- Dashboard Analytics
- Notification
- AI Content Generator

---

# 22. Deliverables

Project menghasilkan:

- REST API
- CMS API
- PostgreSQL Database
- Alembic Migration
- Seeder
- Swagger Documentation
- Repository Pattern
- Service Layer
- API Documentation