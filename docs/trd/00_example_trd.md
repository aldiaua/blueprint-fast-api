Noted. Berarti format standar response kamu menggunakan field `"success": true/false` (bukan `"status": "success"` seperti di draf saya sebelumnya).

Berikut adalah penyesuaian **Technical Requirements Document (TRD)** yang sudah diselaraskan dengan standar API response milikmu.

---

# Technical Requirements Document (TRD)

## Endpoint: Get Active Landing Page Layout

### 1. Deskripsi Singkat

Endpoint ini digunakan oleh aplikasi _frontend_ (Web/Mobile) untuk mengambil struktur tata letak (_layout_) dan konten komponen yang aktif secara dinamis untuk halaman landing tertentu berdasarkan identifier unik (`page_slug`).

---

### 2. Alur Arsitektur Komponen

| Komponen Berkas                               | Peran / Tugas Spesifik                                                                                    |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| **`schemas/landing_page.py`**                 | Memvalidasi parameter `page_slug` dan memastikan struktur _response_ sesuai dengan `LandingPageResponse`. |
| **`api/v1/landing_page.py`**                  | Menangani HTTP GET request pada path `/api/v1/landing-pages/{page_slug}`.                                 |
| **`dependencies/landing_page.py`**            | Menyediakan instance `LandingPageService` beserta database session.                                       |
| **`services/landing_page_service.py`**        | Memeriksa apakah halaman tersedia, mengambil komponen, dan mengurutkannya berdasarkan field `sort_order`. |
| **`repositories/landing_page_repository.py`** | Melakukan query ke database untuk mencari data halaman dan komponen yang berstatus `is_active = true`.    |

---

### 3. Spesifikasi API (API Specification)

- **HTTP Method:** `GET`
- **URL Path:** `/api/v1/landing-pages/{page_slug}`
- **Autentikasi:** No (Public Endpoint)

#### Path Parameters

- `page_slug` (string, required): Slug unik halaman landing (Contoh: `promo-ramadhan`, `home`).

#### Response Sukses (200 OK)

Mengikuti format standar `responses/api_response.py` yang telah ditentukan:

```json
{
    "success": true,
    "message": "Landing page layout retrieved successfully",
    "data": {
        "id": 1,
        "title": "Promo Ramadhan Berkah",
        "slug": "promo-ramadhan",
        "meta_title": "Promo Ramadhan 2026 - Diskon Gede",
        "meta_description": "Dapatkan diskon hingga 70% selama bulan Ramadhan.",
        "components": [
            {
                "id": 101,
                "type": "hero_banner",
                "sort_order": 1,
                "content": {
                    "title": "Sambut Ramadhan dengan Hemat",
                    "image_url": "https://cdn.example.com/banner.png",
                    "cta_link": "/register"
                }
            },
            {
                "id": 102,
                "type": "product_grid",
                "sort_order": 2,
                "content": {
                    "section_title": "Produk Terlaris",
                    "category_id": 5,
                    "limit": 4
                }
            }
        ]
    }
}
```

#### Response Gagal

- **404 Not Found** (Jika slug tidak terdaftar atau tidak aktif)

```json
{
    "success": false,
    "message": "Landing page with slug 'promo-unknown' not found or inactive",
    "data": null
}
```

- **500 Internal Server Error** (Jika terjadi kendala pada database/sistem)

```json
{
    "success": false,
    "message": "Internal server error occurred",
    "data": null
}
```

---

### 4. Aturan Bisnis (Business Rules) & Logika

1. **Validasi Status Halaman:** Sistem hanya boleh mengembalikan data landing page jika field `is_active` pada tabel `landing_pages` bernilai `true`.
2. **Filter Komponen:** Komponen di dalam landing page yang ditarik hanya yang memiliki `is_active = true`. Komponen yang nonaktif tidak boleh bocor ke _response_.
3. **Pengurutan Layout:** Komponen **wajib** diurutkan secara _ascending_ (dari kecil ke besar) berdasarkan field `sort_order`.
4. **Fleksibilitas Konten:** Field `content` di dalam komponen disimpan dalam tipe data `JSONB` di database agar struktur data tiap jenis komponen bisa dinamis tanpa perlu mengubah skema tabel utama.

---

### 5. Rencana Pengujian (Testing Plan)

- **Positive Test Case:**
- Memastikan request dengan slug yang valid dan aktif mengembalikan status `200 OK` dengan `"success": true` beserta seluruh daftar komponen yang berurutan.

- **Negative Test Case:**
- Memastikan request dengan slug yang tidak terdaftar mengembalikan `"success": false` dan status code `404`.
- Memastikan request dengan slug yang terdaftar namun `is_active = false` tetap mengembalikan status `404 Not Found` demi keamanan data.
- Memastikan komponen dengan `is_active = false` tidak ikut dimuat di dalam array `components`.
