# Python Clean Architecture Template

Шаблон проекта на Python с использованием FastAPI и принципов чистой архитектуры.

## Технологии

- **FastAPI** - современный async web framework
- **asyncpg** - высокопроизводительный async драйвер PostgreSQL
- **Pydantic** - валидация данных и настройки
- **PostgreSQL** - БД без использования ORM (чистый SQL)
- **uv** - сверхбыстрый пакетный менеджер (в 10-100 раз быстрее pip) ⚡

## Структура проекта

```
.
├── src/
│   ├── domain/              # Доменный слой (сущности, интерфейсы репозиториев)
│   │   ├── entities/        # Бизнес-сущности
│   │   ├── repositories/    # Интерфейсы репозиториев
│   │   └── exceptions.py    # Доменные исключения
│   │
│   ├── application/         # Слой бизнес-логики
│   │   └── use_cases/       # Use Cases (сценарии использования)
│   │
│   ├── infrastructure/      # Слой инфраструктуры
│   │   ├── database/        # Работа с БД
│   │   ├── repositories/    # Реализации репозиториев
│   │   └── config.py        # Конфигурация
│   │
│   └── presentation/        # Слой представления
│       ├── api/             # FastAPI роутеры и зависимости
│       └── schemas/         # Pydantic схемы для API
│
├── tests/                   # Тесты
├── main.py                  # Точка входа
└── requirements.txt         # Зависимости
```

## Принципы чистой архитектуры

1. **Domain Layer** - независимый от внешних библиотек, содержит бизнес-логику
2. **Application Layer** - содержит use cases, оркеструет бизнес-логику
3. **Infrastructure Layer** - реализации репозиториев, работа с БД без ORM
4. **Presentation Layer** - FastAPI контроллеры, схемы запросов/ответов

## Быстрый старт

### С Docker (рекомендуется) 🐳

```bash
docker compose up
# или
make up
```

Готово! Приложение доступно на http://localhost:8000

📖 Подробнее: [docs/DOCKER.md](docs/DOCKER.md)

---

### Локальная разработка (приложение локально, БД в Docker)

Идеально для разработки с hot-reload:

#### 1. Подними только БД в Docker
```bash
docker compose up db -d
# или
make db
```

#### 2. Установи зависимости

**С uv (рекомендуется, в 10-100 раз быстрее):**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
```

**Или с pip:**
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

#### 3. Создай `.env` файл
```bash
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=cleanarch_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
```

#### 4. Примени миграции
```bash
python -m src.infrastructure.database.migration_runner
```

#### 5. Запусти приложение
```bash
python main.py
# или
make dev
```

Приложение доступно на http://localhost:8000  
БД доступна на localhost:5432

💡 **Быстрый workflow:**
```bash
make db      # запусти БД
make dev     # запусти приложение
```

## 📚 Документация

### API
- **Swagger UI:** http://localhost:8000/docs - интерактивная документация
- **ReDoc:** http://localhost:8000/redoc - альтернативная документация  
- [api.http](api.http) - REST Client для VS Code ⭐
- [docs/API_EXAMPLES.md](docs/API_EXAMPLES.md) - примеры запросов

### Руководства
- [ARCHITECTURE.md](ARCHITECTURE.md) - архитектура проекта
- [docs/DOCKER.md](docs/DOCKER.md) - Docker и docker-compose
- [docs/UV.md](docs/UV.md) - uv пакетный менеджер
- [docs/MIGRATIONS.md](docs/MIGRATIONS.md) - работа с миграциями

### Справочная информация
- [docs/database_libraries_comparison.md](docs/database_libraries_comparison.md) - сравнение библиотек для БД

## 🧪 Тестирование

```bash
pytest
pytest --cov=src tests/  # с покрытием
```

## 🔥 Особенности

- ✅ **Чистая архитектура** - разделение на domain/application/infrastructure/presentation
- ✅ **asyncpg** - максимальная производительность (в 3-5 раз быстрее psycopg2)
- ✅ **Без ORM** - полный контроль над SQL запросами
- ✅ **Connection Pool** - эффективное управление соединениями
- ✅ **Dependency Injection** - через FastAPI Depends
- ✅ **Type Hints** - полная типизация
- ✅ **Repository Pattern** - абстракция работы с данными
- ✅ **Use Cases** - чёткие бизнес-сценарии

## 📝 Примеры API

### REST Client (VS Code) - Рекомендуется! ⭐

Открой `api.http` в VS Code с [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) и кликай "Send Request".

### Автоматический тест

```bash
./scripts/test_api.sh
# или
make api-test
```

### curl команды

```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "name": "John Doe"}'

curl http://localhost:8000/users/1
curl http://localhost:8000/users/
```

📖 Все способы и примеры: [docs/API_EXAMPLES.md](docs/API_EXAMPLES.md)

