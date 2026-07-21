# Technical Requirement Document (TRD)

# 13. Media Upload

| Document | Media Upload API |
|---|---|
| Version | 1.0.0 |
| Status | Draft |
| Authentication | JWT Bearer Token |

---

## 1. Overview

Endpoint ini menyediakan fungsionalitas terpusat untuk mengunggah file media (seperti gambar dan PDF) ke server. Endpoint ini dirancang agar aman, dengan validasi tipe file dan ukuran, serta hanya dapat diakses oleh pengguna yang telah terautentikasi melalui CMS.

---

## 2. Arsitektur

Implementasi ini menggunakan pendekatan layanan tunggal (`MediaService`) yang bertanggung jawab penuh atas logika unggah file, termasuk validasi dan penyimpanan ke sistem file lokal.

### 2.1. Alur Unggah File

```
User (CMS)
    ↓
    │ POST /api/v1/cms/media/upload
    │ Content-Type: multipart/form-data
    │ Authorization: Bearer <jwt_token>
    │ Body: { file: <binary_data> }
    ↓
Auth Middleware (get_current_active_user)
    ├─ Verifikasi JWT Token.
    └─ Lanjutkan jika valid, atau tolak dengan error 401.
    ↓
Media Upload Endpoint
    ├─ Menerima file dari request.
    └─ Memanggil MediaService.save_file(file).
    ↓
MediaService
    ├─ Validasi tipe file (MIME type) dan ukuran file.
    ├─ Membuat nama file unik menggunakan UUID untuk keamanan.
    ├─ Menyimpan file ke direktori lokal (misal: ./uploads/images/).
    └─ Mengembalikan path publik dari file yang telah disimpan.
    ↓
    │ Response: { "success": true, "data": { "url": "/uploads/images/uuid.jpg" } }
    ↓
User (CMS)
```

---

## 3. Spesifikasi API

- **HTTP Method**: `POST`
- **Endpoint**: `/api/v1/cms/media/upload`
- **Autentikasi**: **Wajib**. Memerlukan JWT Bearer Token di header `Authorization`.

### 3.1. Request

- **Header**:
  - `Authorization: Bearer <your_jwt_token>`
- **Body**: `multipart/form-data`
  - `file`: File biner yang akan diunggah.

### 3.2. Response Sukses (201 Created)

Mengembalikan path atau URL publik dari file yang berhasil diunggah.

```json
{
    "success": true,
    "message": "File uploaded successfully",
    "data": {
        "url": "/uploads/images/a1b2c3d4-e5f6-7890-1234-567890abcdef.jpg",
        "filename": "original_filename.jpg",
        "content_type": "image/jpeg",
        "size_kb": 152.7
    }
}
```

### 3.3. Response Gagal

- **400 Bad Request**:
  - Jika tidak ada file yang dikirim: `{"detail": "No file provided."}`
  - Jika tipe file tidak diizinkan: `{"detail": "File type 'application/x-sh' is not allowed."}`
- **401 Unauthorized**: Jika token JWT tidak valid atau tidak ada.
- **413 Request Entity Too Large**: Jika ukuran file melebihi batas yang ditentukan (misal, 5 MB).
- **500 Internal Server Error**: Jika terjadi kesalahan saat proses penyimpanan file.

---

## 4. Aturan Keamanan (Security Rules)

1.  **Autentikasi Ketat**: Endpoint ini dilindungi oleh dependensi `get_current_active_user`.
2.  **Validasi Tipe File (MIME Type)**: Hanya mengizinkan tipe file yang aman dari daftar putih (whitelist) untuk mencegah unggahan file berbahaya.
    - **Whitelist Saat Ini**: `image/jpeg`, `image/png`, `image/webp`, `application/pdf`.
3.  **Validasi Ukuran File**: Menerapkan batas ukuran file maksimum (saat ini 5 MB) untuk mencegah serangan Denial-of-Service (DoS).
4.  **Nama File Unik**: Selalu membuat nama file baru yang unik menggunakan `uuid.uuid4()` untuk mencegah serangan *path traversal* dan konflik nama file. Nama asli dari pengguna tidak pernah digunakan untuk penyimpanan.

---

## 5. Konfigurasi

Konfigurasi path penyimpanan diatur melalui file `.env`.

```env
# Direktori utama untuk menyimpan file yang diunggah
LOCAL_STORAGE_PATH="uploads"
```

Aplikasi akan secara otomatis membuat direktori ini jika belum ada saat startup.

---

## 6. Ketergantungan (Dependencies)

- **`python-multipart`**: Diperlukan oleh FastAPI untuk menangani request `multipart/form-data`.
- **`aiofiles`**: Digunakan untuk operasi I/O file secara asinkron agar tidak memblokir server.

---

## 7. Peningkatan di Masa Depan (Future Improvements)

- **Pencatatan Media**: Menyimpan metadata file (seperti URL, nama file, dan user pengunggah) ke dalam tabel `media` di database untuk manajemen aset yang lebih baik.
- **Endpoint Hapus**: Membuat endpoint `DELETE /api/v1/cms/media` untuk menghapus file dari server.
- **Optimasi Gambar**: Mengimplementasikan kompresi atau perubahan ukuran gambar secara otomatis saat diunggah untuk menghemat ruang penyimpanan dan mempercepat waktu muat.
- **Penyimpanan Cloud**: Mengabstraksi `MediaService` agar dapat beralih ke penyedia penyimpanan cloud seperti AWS S3 melalui konfigurasi.

---