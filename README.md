# Trello Clone — Подробная документация

## Содержание

1. [Обзор проекта](#обзор-проекта)
2. [Технологический стек](#технологический-стек)
3. [Структура проекта](#структура-проекта)
4. [Настройка окружения](#настройка-окружения)
5. [Backend — архитектура и код](#backend--архитектура-и-код)
6. [Frontend — архитектура и код](#frontend--архитектура-и-код)
7. [API Reference](#api-reference)
8. [Как запустить](#как-запустить)

---

## Обзор проекта

Полноценный клон Trello — приложение для управления задачами с:
- Авторизацией (JWT токены)
- Работой с досками (boards)
- Колонками (columns) с Drag & Drop
- Задачами (tasks) с приоритетами и дедлайнами
- Комментариями к задачам
- Поиском и фильтрацией

---

## Технологический стек

| Компонент | Технология | Зачем |
|-----------|-----------|-------|
| Backend | FastAPI | Легковесный async-фреймворк для REST API |
| БД | PostgreSQL | Надёжная реляционная база данных |
| ORM | SQLAlchemy 2.0 | Async ORM для работы с БД |
| Миграции | Alembic | Управление изменениями схемы БД |
| Валидация | Pydantic | Проверка данных на входе/выходе |
| Auth | JWT (python-jose) | Stateless-авторизация через токены |
| Пароли | passlib + bcrypt | Безопасное хеширование паролей |
| Frontend | React 18 + TypeScript | UI-библиотека с типизацией |
| Сборщик | Vite | Быстрая сборка и hot-reload |
| Стили | Tailwind CSS | Utility-first CSS-фреймворк |
| Состояние | Zustand | Лёгкий state management |
| Drag & Drop | @dnd-kit | Современная библиотека DnD |
| HTTP | Axios | Клиент для API-запросов |
| Контейнеры | Docker Compose | Запуск всех сервисов |

---

## Структура проекта

```
trello-clone/
│
├── docker-compose.yml          # Оркестрация контейнеров
├── .env                        # Переменные окружения
├── .gitignore                  # Игнорируемые файлы git
│
├── backend/                    # Python + FastAPI
│   ├── Dockerfile              # Инструкция сборки образа бэкенда
│   ├── requirements.txt        # Python-зависимости
│   ├── alembic.ini             # Конфигурация Alembic
│   │
│   ├── alembic/                # Миграции БД
│   │   ├── env.py              # Скрипт запуска миграций
│   │   ├── script.py.mako      # Шаблон для новых миграций
│   │   └── versions/           # Файлы миграций
│   │
│   └── app/                    # Основное приложение
│       ├── __init__.py         # Делает папку Python-пакетом
│       ├── main.py             # Точка входа FastAPI
│       ├── config.py           # Чтение настроек из .env
│       ├── database.py         # Подключение к PostgreSQL
│       │
│       ├── models/             # SQLAlchemy модели (таблицы БД)
│       │   ├── __init__.py     # Импорт всех моделей
│       │   ├── user.py         # Таблица users
│       │   ├── board.py        # Таблица boards
│       │   ├── column.py       # Таблица columns
│       │   ├── task.py         # Таблица tasks
│       │   └── comment.py      # Таблица comments
│       │
│       ├── schemas/            # Pydantic-схемы (валидация)
│       │   ├── __init__.py
│       │   ├── user.py         # Схемы для пользователей
│       │   ├── board.py        # Схемы для досок
│       │   ├── column.py       # Схемы для колонок
│       │   ├── task.py         # Схемы для задач
│       │   └── comment.py      # Схемы для комментариев
│       │
│       ├── routers/            # API-эндпоинты
│       │   ├── __init__.py
│       │   ├── auth.py         # /api/auth/*
│       │   ├── boards.py       # /api/boards/*
│       │   ├── columns.py      # /api/columns/*
│       │   ├── tasks.py        # /api/tasks/*
│       │   └── comments.py     # /api/comments/*
│       │
│       ├── services/           # Бизнес-логика
│       │   ├── __init__.py
│       │   ├── auth.py         # Хеширование, JWT, поиск пользователя
│       │   └── task.py         # Логика перемещения задач (DnD)
│       │
│       └── utils/              # Утилиты
│           └── dependencies.py # Depends: get_current_user, get_db
│
└── frontend/                   # React + TypeScript
    ├── Dockerfile              # Инструкция сборки образа фронтенда
    ├── package.json            # npm-зависимости
    ├── vite.config.ts          # Конфигурация Vite
    ├── tsconfig.json           # Настройки TypeScript
    ├── tailwind.config.js      # Конфигурация Tailwind CSS
    ├── postcss.config.js       # PostCSS плагины
    ├── index.html              # Главный HTML-файл SPA
    │
    └── src/
        ├── main.tsx            # Точка входа React
        ├── App.tsx             # Роутинг (Routes)
        ├── index.css           # Глобальные стили (Tailwind)
        │
        ├── types/
        │   └── index.ts        # TypeScript-интерфейсы
        │
        ├── api/
        │   └── axios.ts        # Axios instance + interceptors
        │
        ├── store/
        │   └── authStore.ts    # Zustand: состояние авторизации
        │
        ├── hooks/
        │   ├── useAuth.ts      # Хук для авторизации
        │   └── useTasks.ts     # Хук для работы с задачами
        │
        └── components/
            ├── Auth/
            │   ├── LoginForm.tsx      # Форма входа
            │   └── RegisterForm.tsx   # Форма регистрации
            │
            ├── Board/
            │   ├── BoardView.tsx      # Основной вид доски
            │   ├── Column.tsx         # Одна колонка
            │   └── TaskCard.tsx       # Карточка задачи
            │
            ├── Task/
            │   ├── TaskModal.tsx      # Модалка редактирования задачи
            │   └── CommentSection.tsx # Секция комментариев
            │
            └── UI/
                ├── Button.tsx         # Универсальная кнопка
                └── Input.tsx          # Универсальное поле ввода
```

---

## Настройка окружения

### Файл `.env`

```env
# PostgreSQL
POSTGRES_USER=trello_user          # Имя пользователя БД
POSTGRES_PASSWORD=trello_pass_2024 # Пароль пользователя БД
POSTGRES_DB=trello_db              # Имя базы данных

# URL подключения к БД (asyncpg драйвер)
DATABASE_URL=postgresql+asyncpg://trello_user:trello_pass_2024@postgres:5432/trello_db

# JWT настройки
SECRET_KEY=trello-clone-secret-key-change-in-production-2024  # Секрет для подписи токенов
ALGORITHM=HS256                      # Алгоритм шифрования
ACCESS_TOKEN_EXPIRE_MINUTES=30       # Время жизни access-токена
REFRESH_TOKEN_EXPIRE_DAYS=7          # Время жизни refresh-токена
```

---

## Backend — архитектура и код

### 1. `app/main.py` — Точка входа

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Импорт всех роутеров (endpoints)
from app.routers import auth, boards, columns, tasks, comments

# Создание экземпляра FastAPI — это наше приложение
app = FastAPI(title="Trello Clone API", version="1.0.0")

# CORS middleware — разрешает фронтенду (localhost:3000) делать запросы к бэкенду
# Без этого браузер блокирует запросы с другого порта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,   # Разрешает cookie
    allow_methods=["*"],      # Разрешает все HTTP-методы (GET, POST, PUT, DELETE)
    allow_headers=["*"],      # Разрешает все заголовки
)

# Подключение роутеров — каждый обрабатывает свою группу URL
app.include_router(auth.router)       # /api/auth/*
app.include_router(boards.router)     # /api/boards/*
app.include_router(columns.router)    # /api/columns/*
app.include_router(tasks.router)      # /api/tasks/*
app.include_router(comments.router)   # /api/tasks/{id}/comments/*

# Health check endpoint — проверка что сервер работает
@app.get("/api/health")
async def health_check():
    return {"status": "ok"}
```

---

### 2. `app/config.py` — Конфигурация

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

# BaseSettings автоматически читает переменные из .env файла
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://..."  # URL БД
    SECRET_KEY: str = "..."                          # Секрет для JWT
    ALGORITHM: str = "HS256"                         # Алгоритм шифрования
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30            # Access token живёт 30 мин
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7               # Refresh token живёт 7 дней

    class Config:
        env_file = ".env"  # Читать настройки из .env файла

# @lru_cache кэширует результат — Settings создаётся только один раз
@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

---

### 3. `app/database.py` — Подключение к БД

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings
settings = get_settings()

# create_async_engine — создаёт async-подключение к PostgreSQL
# echo=False — не логировать каждый SQL-запрос (для продакшена)
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# async_sessionmaker — фабрика сессий
# class_=AsyncSession — используем async-сессии
# expire_on_commit=False — данные не сбрасываются после commit
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Base — базовый класс для всех SQLAlchemy моделей
# Все модели (User, Board, Column...) наследуются от него
class Base(DeclarativeBase):
    pass

# get_db — dependency injection для FastAPI
# Создаёт сессию, передаёт в endpoint, потом коммитит/откатывает
async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session           # Передаём сессию в endpoint
            await session.commit()  # Коммитим изменения при успехе
        except Exception:
            await session.rollback()  # Откатываем при ошибке
            raise
```

---

### 4. `app/models/` — SQLAlchemy модели

#### `models/user.py` — Таблица пользователей

```python
import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"  # Имя таблицы в БД

    # id — первичный ключ, UUID строка, генерируется автоматически
    id: Mapped[str] = mapped_column(
        String(36),                          # Максимальная длина 36 символов
        primary_key=True,                    # Это первичный ключ
        default=lambda: str(uuid.uuid4())   # Генерируем UUID при создании
    )

    # email — уникальный email, индекс для быстрого поиска
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,        # Нельзя有两个 одинаковых email
        nullable=False,     # Не может быть пустым
        index=True          # индекс для быстрого поиска по email
    )

    # username — имя пользователя
    username: Mapped[str] = mapped_column(String(100), nullable=False)

    # password_hash — хеш пароля (НИКОГДА не храним пароль в открытом виде)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)

    # created_at — дата создания (автоматически при создании записи)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)  # UTC время
    )

    # updated_at — дата обновления (обновляется при каждом изменении)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)  # Автоматически при обновлении
    )

    # Связи (relationships):
    # user.boards — список досок пользователя
    # cascade="all, delete-orphan" — при удалении пользователя удаляются его доски
    boards = relationship("Board", back_populates="owner", cascade="all, delete-orphan")

    # user.comments — список комментариев пользователя
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
```

#### `models/board.py` — Таблица досок

```python
class Board(Base):
    __tablename__ = "boards"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)           # Название доски
    description: Mapped[str | None] = mapped_column(Text, nullable=True)      # Описание (опционально)

    # owner_id — внешний ключ на таблицу users
    # ondelete="CASCADE" — при удалении пользователя удаляются его доски
    owner_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Связи:
    owner = relationship("User", back_populates="boards")  # Владелец доски
    # columns — колонки доски, отсортированные по order_position
    columns = relationship("Column", back_populates="board", cascade="all, delete-orphan", order_by="Column.order_position")
```

#### `models/column.py` — Таблица колонок

```python
class Column(Base):
    __tablename__ = "columns"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)  # "To Do", "In Progress", "Done"

    # board_id — колонка принадлежит доске
    board_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("boards.id", ondelete="CASCADE"),
        nullable=False
    )

    # order_position — позиция колонки (для Drag & Drop)
    # Используем integer чтобы менять порядок без пересчёта всей таблицы
    order_position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    board = relationship("Board", back_populates="columns")
    # tasks — задачи колонки, отсортированные по order_position
    tasks = relationship("Task", back_populates="column", cascade="all, delete-orphan", order_by="Task.order_position")
```

#### `models/task.py` — Таблица задач

```python
import enum

# PriorityEnum — перечисление приоритетов задачи
class PriorityEnum(str, enum.Enum):
    low = "low"        # Низкий приоритет
    medium = "medium"  # Средний приоритет
    high = "high"      # Высокий приоритет

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)           # Название задачи
    description: Mapped[str | None] = mapped_column(Text, nullable=True)      # Описание

    # column_id — задача принадлежит колонке
    column_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("columns.id", ondelete="CASCADE"),
        nullable=False
    )

    # order_position — позиция задачи внутри колонки (для Drag & Drop)
    order_position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # priority — приоритет (enum: low, medium, high)
    priority: Mapped[PriorityEnum] = mapped_column(
        SAEnum(PriorityEnum),
        default=PriorityEnum.medium,  # По умолчанию средний
        nullable=False
    )

    # deadline — дедлайн (nullable — может быть не установлен)
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # author_id — кто создал задачу
    author_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    column = relationship("Column", back_populates="tasks")  # Колонка задачи
    author = relationship("User")                              # Автор задачи
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan", order_by="Comment.created_at")
```

#### `models/comment.py` — Таблица комментариев

```python
class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    content: Mapped[str] = mapped_column(Text, nullable=False)  # Текст комментария

    task_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False
    )

    author_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    task = relationship("Task", back_populates="comments")   # Задача
    author = relationship("User", back_populates="comments")  # Автор
```

---

### 5. `app/schemas/` — Pydantic-схемы

Схемы определяют **какие данные** принимают и возвращают endpoints.

#### `schemas/user.py`

```python
from pydantic import BaseModel

# UserCreate — схема для регистрации
# Принимает: email, username, password
class UserCreate(BaseModel):
    email: str
    username: str
    password: str

# UserLogin — схема для входа
class UserLogin(BaseModel):
    email: str
    password: str

# UserResponse — схема ответа (без пароля!)
# Отдаёт: id, email, username, created_at
class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    created_at: datetime

    # from_attributes=True — позволяет создать из SQLAlchemy объекта
    model_config = {"from_attributes": True}

# TokenResponse — схема JWT-токенов
class TokenResponse(BaseModel):
    access_token: str    # Токен доступа (30 мин)
    refresh_token: str   # Токен обновления (7 дней)
    token_type: str = "bearer"  # Тип токена

# TokenRefresh — схема для обновления токена
class TokenRefresh(BaseModel):
    refresh_token: str
```

#### `schemas/task.py`

```python
from app.models.task import PriorityEnum

# TaskCreate — схема создания задачи
class TaskCreate(BaseModel):
    title: str                              # Обязательное поле
    description: str | None = None          # Опциональное
    column_id: str                          # В какой колонке
    priority: PriorityEnum = PriorityEnum.medium  # По умолчанию medium
    deadline: datetime | None = None        # Опционально

# TaskUpdate — схема обновления (все поля опциональные)
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: PriorityEnum | None = None
    deadline: datetime | None = None

# TaskMove — схема перемещения задачи (Drag & Drop)
class TaskMove(BaseModel):
    column_id: str    # Новая колонка
    order_position: int  # Новая позиция

# TaskResponse — полная схема задачи для ответа
class TaskResponse(BaseModel):
    id: str
    title: str
    description: str | None
    column_id: str
    order_position: int
    priority: PriorityEnum
    deadline: datetime | None
    author_id: str
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
```

---

### 6. `app/services/auth.py` — Сервис аутентификации

```python
from passlib.context import CryptContext
from jose import JWTError, jwt

# pwd_context — контекст для хеширования паролей
# bcrypt — алгоритм хеширования (медленный = безопасный)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hash_password — хеширует пароль
# "my_password" → "$2b$12$KIXQ1234..."
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# verify_password — проверяет пароль
# Сравнивает "my_password" с хешем "$2b$12$KIXQ1234..."
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# create_access_token — создаёт JWT access token
# Живёт 30 минут, содержит email пользователя
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# create_refresh_token — создаёт JWT refresh token
# Живёт 7 дней, используется для получения нового access token
def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# decode_token — декодирует JWT токен
# Возвращает payload или None если токен невалидный
def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
```

---

### 7. `app/services/task.py` — Логика Drag & Drop

```python
# move_task — перемещает задачу между колонками
# Алгоритм:
# 1. Находим задачу
# 2. Определяем старую и новую позицию
# 3. Сдвигаем остальные задачи в старой колонке
# 4. Сдвигаем задачи в новой колонке
# 5. Обновляем позицию перемещаемой задачи
async def move_task(db, task_id, new_column_id, new_order_position, user_id):
    # Находим задачу по id
    task = await db.execute(select(Task).where(Task.id == task_id))
    task = task.scalar_one_or_none()

    old_column_id = task.column_id
    old_order_position = task.order_position

    # Если задача остаётся в той же колонке
    if old_column_id == new_column_id:
        if old_order_position < new_order_position:
            # Двигаем вниз: сдвигаем задачи вверх
            await db.execute(
                update(Task).where(
                    Task.column_id == old_column_id,
                    Task.order_position > old_order_position,
                    Task.order_position <= new_order_position,
                    Task.id != task_id,
                ).values(order_position=Task.order_position - 1)
            )
        elif old_order_position > new_order_position:
            # Двигаем вверх: сдвигаем задачи вниз
            await db.execute(
                update(Task).where(
                    Task.column_id == old_column_id,
                    Task.order_position >= new_order_position,
                    Task.order_position < old_order_position,
                    Task.id != task_id,
                ).values(order_position=Task.order_position + 1)
            )
    else:
        # Задача переходит в другую колонку
        # Сдвигаем вверх в старой колонке
        await db.execute(
            update(Task).where(
                Task.column_id == old_column_id,
                Task.order_position > old_order_position,
            ).values(order_position=Task.order_position - 1)
        )
        # Сдвигаем вниз в новой колонке
        await db.execute(
            update(Task).where(
                Task.column_id == new_column_id,
                Task.order_position >= new_order_position,
            ).values(order_position=Task.order_position + 1)
        )

    # Обновляем позицию задачи
    task.column_id = new_column_id
    task.order_position = new_order_position
    return task
```

---

### 8. `app/utils/dependencies.py` — Dependency Injection

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

# security — извлекает Bearer token из заголовка Authorization
security = HTTPBearer()

# get_current_user — dependency для FastAPI
# 1. Извлекает токен из заголовка
# 2. Декодирует JWT
# 3. Находит пользователя в БД
# 4. Возвращает объект User
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials  # Извлекаем строку токена
    payload = decode_token(token)    # Декодируем JWT

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")

    email = payload.get("sub")  # sub — это email пользователя
    user = await get_user_by_email(db, email)

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user
```

---

### 9. `app/routers/auth.py` — Эндпоинты авторизации

```python
router = APIRouter(prefix="/api/auth", tags=["auth"])

# POST /api/auth/register — регистрация нового пользователя
@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем не занят ли email
    existing = await get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Создаём пользователя (пароль хешируется автоматически)
    user = await create_user(db, data.email, data.username, data.password)
    return user

# POST /api/auth/login — вход в систему
@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, data.email)

    # Проверяем email и пароль
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Создаём JWT токены
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

# POST /api/auth/refresh — обновление access token
@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: TokenRefresh, db: AsyncSession = Depends(get_db)):
    payload = decode_token(data.refresh_token)

    # Проверяем refresh token
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    email = payload.get("sub")
    user = await get_user_by_email(db, email)

    # Создаём новую пару токенов
    access_token = create_access_token({"sub": user.email})
    new_refresh_token = create_refresh_token({"sub": user.email})

    return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)

# GET /api/auth/me — получение текущего пользователя
@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

---

### 10. `app/routers/boards.py` — Эндпоинты досок

```python
router = APIRouter(prefix="/api/boards", tags=["boards"])

# Дефолтные колонки при создании доски
DEFAULT_COLUMNS = ["To Do", "In Progress", "Done"]

# GET /api/boards — список всех досок пользователя
@router.get("", response_model=BoardListResponse)
async def list_boards(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),  # Требует авторизации
):
    result = await db.execute(
        select(Board)
        .where(Board.owner_id == current_user.id)  # Только доски пользователя
        .order_by(Board.created_at.desc())           # Новые первыми
    )
    boards = result.scalars().all()
    return BoardListResponse(boards=boards, total=len(boards))

# POST /api/boards — создание новой доски
@router.post("", response_model=BoardResponse, status_code=201)
async def create_board(
    data: BoardCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Создаём доску
    board = Board(title=data.title, description=data.description, owner_id=current_user.id)
    db.add(board)
    await db.flush()  # flush чтобы получить id доски

    # Создаём 3 дефолтные колонки
    for i, col_title in enumerate(DEFAULT_COLUMNS):
        column = Column(title=col_title, board_id=board.id, order_position=i)
        db.add(column)

    await db.flush()
    return board

# GET /api/boards/{board_id} — получение конкретной доски
@router.get("/{board_id}", response_model=BoardResponse)
async def get_board(board_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Board).where(Board.id == board_id, Board.owner_id == current_user.id)
    )
    board = result.scalar_one_or_none()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board

# DELETE /api/boards/{board_id} — удаление доски
@router.delete("/{board_id}", status_code=204)
async def delete_board(board_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(
        select(Board).where(Board.id == board_id, Board.owner_id == current_user.id)
    )
    board = result.scalar_one_or_none()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    await db.delete(board)
    await db.flush()
```

---

## Frontend — архитектура и код

### 1. `src/types/index.ts` — TypeScript-интерфейсы

```typescript
// Определяем типы данных которые приходят с бэкенда

export interface User {
  id: string;
  email: string;
  username: string;
  created_at: string;
}

export interface Board {
  id: string;
  title: string;
  description: string | null;
  owner_id: string;
  created_at: string;
  updated_at: string;
}

export interface Column {
  id: string;
  title: string;
  board_id: string;
  order_position: number;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: string;
  title: string;
  description: string | null;
  column_id: string;
  order_position: number;
  priority: 'low' | 'medium' | 'high';  // Union type — одно из трёх
  deadline: string | null;
  author_id: string;
  created_at: string;
  updated_at: string;
}

export interface Comment {
  id: string;
  content: string;
  task_id: string;
  author_id: string;
  created_at: string;
  updated_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}
```

---

### 2. `src/api/axios.ts` — HTTP-клиент

```typescript
import axios from 'axios';

// Создаём экземпляр axios с базовым URL
const api = axios.create({
  baseURL: '/api',  // Все запросы будут к /api/*
  headers: { 'Content-Type': 'application/json' },
});

// Request interceptor — добавляет JWT токен к каждому запросу
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;  // Заголовок Authorization
  }
  return config;
});

// Response interceptor — обрабатывает 401 ошибку
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Если получили 401 и это не повторный запрос
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');

      if (refreshToken) {
        try {
          // Пробуем обновить access token
          const response = await axios.post('/api/auth/refresh', {
            refresh_token: refreshToken,
          });
          const { access_token, refresh_token } = response.data;

          // Сохраняем новые токены
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);

          // Повторяем оригинальный запрос с новым токеном
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        } catch {
          // Если refresh тоже истёк — разлогиниваем
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

export default api;
```

---

### 3. `src/store/authStore.ts` — Zustand store

```typescript
import { create } from 'zustand';
import api from '../api/axios';

// AuthState — состояние авторизации
interface AuthState {
  user: User | null;          // Текущий пользователь (null если не авторизован)
  isAuthenticated: boolean;   // Авторизован ли пользователь
  isLoading: boolean;         // Идёт ли загрузка

  login: (email: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

// create<AuthState> — создаём Zustand store с типизацией
export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,  // Начинаем с загрузки

  login: async (email, password) => {
    // Отправляем POST /api/auth/login
    const response = await api.post('/auth/login', { email, password });
    const { access_token, refresh_token } = response.data;

    // Сохраняем токены в localStorage
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);

    // Получаем данные пользователя
    const userResponse = await api.get('/auth/me');
    set({ user: userResponse.data, isAuthenticated: true });
  },

  register: async (email, username, password) => {
    await api.post('/auth/register', { email, username, password });
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    set({ user: null, isAuthenticated: false });
  },

  checkAuth: async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      set({ isLoading: false });
      return;
    }
    try {
      const response = await api.get('/auth/me');
      set({ user: response.data, isAuthenticated: true, isLoading: false });
    } catch {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      set({ isLoading: false });
    }
  },
}));
```

---

### 4. `src/components/Board/BoardView.tsx` — Основной компонент доски

```tsx
// DndContext — контекст Drag & Drop от @dnd-kit
import { DndContext, DragOverlay, closestCorners } from '@dnd-kit/core';

export function BoardView() {
  const { boardId } = useParams();  // ID доски из URL
  const [tasks, setTasks] = useState<Task[]>([]);
  const [activeTask, setActiveTask] = useState<Task | null>(null);

  // handleDragStart — вызывается когда начинаем перетаскивать
  const handleDragStart = (event: DragStartEvent) => {
    const task = tasks.find((t) => t.id === event.active.id);
    if (task) setActiveTask(task);  # Сохраняем перетаскиваемую задачу
  };

  // handleDragEnd — вызывается когда отпустили задачу
  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event;
    if (!over) return;

    const activeId = active.id as string;
    const overId = over.id as string;

    // Определяем новую колонку и позицию
    let targetColumnId: string;
    let newOrder: number;

    const overTask = tasks.find((t) => t.id === overId);
    if (overTask) {
      // Упали на другую задачу — берём её колонку
      targetColumnId = overTask.column_id;
    } else {
      // Упали на колонку — берём её id
      targetColumnId = overId;
    }

    // Отправляем PATCH /api/tasks/{id}/move
    await api.patch(`/tasks/${activeId}/move`, {
      column_id: targetColumnId,
      order_position: newOrder,
    });

    // Обновляем список задач
    await fetchBoardData();
  };

  return (
    // DndContext — оборачивает всё что участвует в DnD
    <DndContext
      sensors={sensors}
      collisionDetection={closestCorners}  # Определяет куда упала задача
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
    >
      <div className="flex gap-4">
        {columns.map((column) => (
          <Column key={column.id} column={column} tasks={...} />
        ))}
      </div>

      {/* DragOverlay — отрисовка перетаскиваемой задачи */}
      <DragOverlay>
        {activeTask && <TaskCard task={activeTask} onClick={() => {}} />}
      </DragOverlay>
    </DndContext>
  );
}
```

---

### 5. `src/components/Board/TaskCard.tsx` — Карточка задачи

```tsx
import { useSortable } from '@dnd-kit/sortable';

export function TaskCard({ task, onClick }: TaskCardProps) {
  // useSortable — делает элемент перетаскиваемым
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({
    id: task.id,  // Уникальный ID задачи
    data: { type: 'task', task },  # Данные для определения типа
  });

  // CSS Transform для анимации перетаскивания
  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div
      ref={setNodeRef}        # Ссылка на DOM-элемент
      style={style}           # CSS трансформации
      {...attributes}         # ARIA атрибуты
      {...listeners}          # Обработчики drag-and-drop
      onClick={() => onClick(task)}
      className={`... ${isDragging ? 'opacity-50' : ''}`}
    >
      <h4>{task.title}</h4>
      <span className={priorityColors[task.priority]}>{task.priority}</span>
    </div>
  );
}
```

---

### 6. `src/components/Board/Column.tsx` — Колонка

```tsx
import { useDroppable } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';

export function Column({ column, tasks, onTaskClick, onAddTask }: ColumnProps) {
  // useDroppable — делает колонку целью для сброса
  const { setNodeRef, isOver } = useDroppable({
    id: column.id,  // ID колонки
    data: { type: 'column', column },
  });

  return (
    <div ref={setNodeRef} className={`bg-gray-100 ... ${isOver ? 'ring-2 ring-blue-500' : ''}`}>
      <h3>{column.title}</h3>

      {/* SortableContext — контекст сортировки внутри колонки */}
      <SortableContext items={tasks.map((t) => t.id)} strategy={verticalListSortingStrategy}>
        <div className="space-y-2">
          {tasks.map((task) => (
            <TaskCard key={task.id} task={task} onClick={onTaskClick} />
          ))}
        </div>
      </SortableContext>
    </div>
  );
}
```

---

## API Reference

### Auth

| Метод | URL | Описание | Тело запроса |
|-------|-----|----------|-------------|
| POST | `/api/auth/register` | Регистрация | `{email, username, password}` |
| POST | `/api/auth/login` | Вход | `{email, password}` |
| POST | `/api/auth/refresh` | Обновление токена | `{refresh_token}` |
| GET | `/api/auth/me` | Текущий пользователь | — |

### Boards

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/boards` | Список досок |
| POST | `/api/boards` | Создать доску |
| GET | `/api/boards/{id}` | Получить доску |
| PUT | `/api/boards/{id}` | Обновить доску |
| DELETE | `/api/boards/{id}` | Удалить доску |

### Columns

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/boards/{id}/columns` | Список колонок |
| POST | `/api/boards/{id}/columns` | Создать колонку |
| PUT | `/api/columns/{id}` | Обновить колонку |
| DELETE | `/api/columns/{id}` | Удалить колонку |

### Tasks

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/boards/{id}/tasks` | Список задач доски |
| POST | `/api/columns/{id}/tasks` | Создать задачу |
| GET | `/api/tasks/{id}` | Получить задачу |
| PUT | `/api/tasks/{id}` | Обновить задачу |
| PATCH | `/api/tasks/{id}/move` | Переместить задачу (DnD) |
| DELETE | `/api/tasks/{id}` | Удалить задачу |

### Comments

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/tasks/{id}/comments` | Список комментариев |
| POST | `/api/tasks/{id}/comments` | Добавить комментарий |
| PUT | `/api/tasks/{id}/comments/{id}` | Обновить комментарий |
| DELETE | `/api/tasks/{id}/comments/{id}` | Удалить комментарий |

---

## Как запустить

### 1. Установите Docker

Скачайте и установите [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 2. Клонируйте проект

```bash
git clone <repository-url>
cd trello-clone
```

### 3. Запустите контейнеры

```bash
docker-compose up --build
```

### 4. Откройте в браузере

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs (Swagger UI)

### 5. Создайте аккаунт

1. Перейдите на http://localhost:3000/register
2. Введите email, имя, пароль
3. Войдите на http://localhost:3000/login
4. Создайте доску и начните работать!

---

## Полезные команды

```bash
# Запуск в фоне
docker-compose up -d --build

# Просмотр логов
docker-compose logs -f backend

# Остановка всех контейнеров
docker-compose down

# Удаление данных БД
docker-compose down -v

# Выполнить команду в контейнере
docker-compose exec backend python -c "from app.database import engine; print(engine)"
```
