from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class StudentItem(BaseModel):
    """Student item for list responses."""
    
    uuid: UUID
    full_name: str = Field(..., description="Nama lengkap siswa")
    nick_name: Optional[str] = Field(None, description="Nama panggilan")
    photo: Optional[str] = Field(None, description="Foto profil")
    quote: Optional[str] = Field(None, description="Quote")

    class Config:
        from_attributes = True


class StudentDetail(BaseModel):
    """Student detail response."""
    
    uuid: UUID
    class_id: int
    nis: Optional[str] = Field(None, description="Nomor induk siswa")
    full_name: str = Field(..., description="Nama lengkap")
    nick_name: Optional[str] = Field(None, description="Nama panggilan")
    gender: Optional[str] = Field(None, description="Jenis kelamin")
    birth_place: Optional[str] = Field(None, description="Tempat lahir")
    birth_date: Optional[str] = Field(None, description="Tanggal lahir")
    address: Optional[str] = Field(None, description="Alamat")
    hobby: Optional[str] = Field(None, description="Hobi")
    ambition: Optional[str] = Field(None, description="Cita-cita")
    quote: Optional[str] = Field(None, description="Quote")
    photo: Optional[str] = Field(None, description="Foto profil")
    cover_image: Optional[str] = Field(None, description="Cover image")
    instagram: Optional[str] = Field(None, description="Instagram handle")
    tiktok: Optional[str] = Field(None, description="TikTok handle")
    email: Optional[str] = Field(None, description="Email")
    phone: Optional[str] = Field(None, description="Nomor HP")
    sort_order: int = Field(default=0, description="Urutan")
    created_at: Optional[datetime] = Field(None, description="Waktu dibuat")
    updated_at: Optional[datetime] = Field(None, description="Waktu diubah")

    class Config:
        from_attributes = True


class StudentCreate(BaseModel):
    class_uuid: str
    nis: Optional[str] = None
    full_name: str
    nick_name: Optional[str] = None
    gender: Optional[str] = None
    birth_place: Optional[str] = None
    birth_date: Optional[str] = None
    address: Optional[str] = None
    hobby: Optional[str] = None
    ambition: Optional[str] = None
    quote: Optional[str] = None
    photo: Optional[str] = None
    cover_image: Optional[str] = None
    instagram: Optional[str] = None
    tiktok: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    sort_order: Optional[int] = Field(default=0, ge=0)
    is_active: Optional[bool] = True


class StudentUpdate(BaseModel):
    class_uuid: Optional[str] = None
    nis: Optional[str] = None
    full_name: Optional[str] = None
    nick_name: Optional[str] = None
    gender: Optional[str] = None
    birth_place: Optional[str] = None
    birth_date: Optional[str] = None
    address: Optional[str] = None
    hobby: Optional[str] = None
    ambition: Optional[str] = None
    quote: Optional[str] = None
    photo: Optional[str] = None
    cover_image: Optional[str] = None
    instagram: Optional[str] = None
    tiktok: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    sort_order: Optional[int] = Field(default=None, ge=0)
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True
