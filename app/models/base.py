from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid as uuid_lib


class Base(DeclarativeBase):
    pass


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[uuid_lib.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, nullable=False, default=uuid_lib.uuid4
    )
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    position: Mapped[str] = mapped_column(String(150), nullable=False)
    subject: Mapped[str | None] = mapped_column(String(150), nullable=True)
    quote: Mapped[str | None] = mapped_column(Text, nullable=True)
    biography: Mapped[str | None] = mapped_column(Text, nullable=True)
    photo: Mapped[str | None] = mapped_column(Text, nullable=True)
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    instagram: Mapped[str | None] = mapped_column(String(255), nullable=True)
    linkedin: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    classes: Mapped[list["Class"]] = relationship("Class", back_populates="homeroom_teacher")

    def __repr__(self) -> str:
        return f"<Teacher(id={self.id}, uuid={self.uuid}, name={self.name}, position={self.position})>"


class Class(Base):
    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[uuid_lib.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, nullable=False, default=uuid_lib.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    cover_image: Mapped[str | None] = mapped_column(Text, nullable=True)
    homeroom_teacher_id: Mapped[int | None] = mapped_column(
        ForeignKey("teachers.id"), nullable=True
    )
    graduation_year: Mapped[int] = mapped_column(Integer, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    homeroom_teacher: Mapped[Teacher | None] = relationship("Teacher", back_populates="classes")
    students: Mapped[list["Student"]] = relationship("Student", back_populates="class_info")

    def __repr__(self) -> str:
        return f"<Class(id={self.id}, uuid={self.uuid}, name={self.name}, graduation_year={self.graduation_year})>"


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[uuid_lib.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, nullable=False, default=uuid_lib.uuid4
    )
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)
    nis: Mapped[str | None] = mapped_column(String(50), nullable=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    nick_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(10), nullable=True)
    birth_place: Mapped[str | None] = mapped_column(String(100), nullable=True)
    birth_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    hobby: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ambition: Mapped[str | None] = mapped_column(String(255), nullable=True)
    quote: Mapped[str | None] = mapped_column(Text, nullable=True)
    photo: Mapped[str | None] = mapped_column(Text, nullable=True)
    cover_image: Mapped[str | None] = mapped_column(Text, nullable=True)
    instagram: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tiktok: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    class_info: Mapped[Class] = relationship("Class", back_populates="students")

    def __repr__(self) -> str:
        return f"<Student(id={self.id}, uuid={self.uuid}, full_name={self.full_name})>"


class Setting(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    setting_key: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    components: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    styles: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Setting(id={self.id}, setting_key={self.setting_key})>"


class PageSection(Base):
    __tablename__ = "page_sections"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[uuid_lib.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, nullable=False, default=uuid_lib.uuid4
    )
    section_type: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    components: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    styles: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<PageSection(id={self.id}, section_type={self.section_type}, title={self.title})>"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[uuid_lib.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, nullable=False, default=uuid_lib.uuid4
    )
    username: Mapped[str] = mapped_column(String(127), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="admin")  # admin, editor, viewer, superadmin
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, uuid={self.uuid}, username={self.username}, role={self.role})>"
