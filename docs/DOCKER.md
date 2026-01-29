# Docker - Быстрый запуск

## 🚀 Запуск одной командой

```bash
docker compose up
```

Или через Makefile:
```bash
make up
```

Это запустит:
- ✅ PostgreSQL 15 на порту 5432
- ✅ Применит миграции автоматически
- ✅ Запустит FastAPI приложение на порту 8000

Приложение доступно: http://localhost:8000

---

## ⚡ Makefile команды

```bash
make help     # показать все команды
make up       # запустить всё
make down     # остановить
make logs     # логи
make build    # пересобрать
make migrate  # запустить миграции
make status   # статус миграций
make test     # тесты
```

---

## 📋 Основные команды

### Запустить (с логами)
```bash
docker compose up
```

### Запустить в фоне
```bash
docker compose up -d
```

### Остановить
```bash
docker compose down
```

### Остановить и удалить данные
```bash
docker compose down -v
```

### Пересобрать образ
```bash
docker compose build
docker compose up
```

### Посмотреть логи
```bash
docker compose logs
docker compose logs app
docker compose logs db
```

### Логи в реальном времени
```bash
docker compose logs -f
```

---

## 🔧 Разработка

### Только БД в Docker (рекомендуется для разработки)

Самый удобный режим - БД в Docker, приложение локально:

```bash
# Подними только БД
docker compose up db -d

# В другом терминале - запусти приложение локально
source .venv/bin/activate
python main.py
```

**Преимущества:**
- ✅ Быстрый перезапуск приложения
- ✅ Легко дебажить
- ✅ Hot-reload работает мгновенно
- ✅ Не нужно пересобирать Docker образ

### Всё в Docker

Файлы монтируются в контейнер - изменения применяются автоматически.

```bash
docker compose up
```

Измени код → сохрани → сервер перезапустится автоматически.

### Выполнить команду в контейнере

```bash
docker compose exec app python -m pytest
docker compose exec app python -m src.infrastructure.database.migration_runner status
docker compose exec db psql -U postgres -d cleanarch_db
```

### Подключиться к БД

```bash
docker compose exec db psql -U postgres -d cleanarch_db
```

SQL команды:
```sql
\dt                              -- список таблиц
select * from users;             -- данные
select * from schema_migrations; -- применённые миграции
```

---

## 🗄️ Данные

### Где хранятся данные?

Данные PostgreSQL хранятся в Docker volume `postgres_data`.

### Очистить данные

```bash
docker compose down -v
```

Это удалит все данные БД. При следующем запуске всё начнётся с чистого листа.

### Backup данных

```bash
docker compose exec db pg_dump -U postgres cleanarch_db > backup.sql
```

### Восстановить данные

```bash
cat backup.sql | docker compose exec -T db psql -U postgres -d cleanarch_db
```

---

## 🐛 Troubleshooting

### Порт 5432 уже занят

Если у вас локально запущен PostgreSQL:

**Вариант 1:** Остановить локальный PostgreSQL
```bash
brew services stop postgresql
```

**Вариант 2:** Изменить порт в docker-compose.yml
```yaml
ports:
  - "5433:5432"  # внешний порт 5433
```

### Порт 8000 уже занят

Измени порт в docker-compose.yml:
```yaml
ports:
  - "8001:8000"
```

Приложение будет доступно на http://localhost:8001

### Контейнер падает с ошибкой

Посмотри логи:
```bash
docker compose logs app
```

### Пересоздать всё с нуля

```bash
docker compose down -v
docker compose build --no-cache
docker compose up
```

---

## 🏗️ Production готовность

Для production измени:

### 1. Переменные окружения

Создай `.env.production`:
```
DATABASE_PASSWORD=strong_password_here
DEBUG=False
```

Запусти:
```bash
docker compose --env-file .env.production up
```

### 2. Используй отдельную БД

Убери `db` из docker-compose и подключайся к внешней БД:
```yaml
app:
  environment:
    DATABASE_HOST: your-db-host.com
    DATABASE_PASSWORD: ${DB_PASSWORD}
```

### 3. Добавь Nginx

Создай `nginx.conf` и добавь сервис в docker-compose.

---

## 📦 Размеры образов

```bash
docker images | grep cleanarch
```

Ожидаемый размер:
- `cleanarch_app`: ~200MB
- `postgres:15-alpine`: ~230MB

---

## 🎯 Быстрые команды

### С Makefile
```bash
make up          # запустить
make down        # остановить
make logs        # логи
make migrate     # миграции
make test        # тесты
```

### Docker Compose напрямую
```bash
docker compose up -d              # запустить в фоне
docker compose down               # остановить
docker compose logs -f app        # логи приложения
docker compose exec app bash      # войти в контейнер
docker compose exec db psql -U postgres -d cleanarch_db  # БД
docker compose restart app        # перезапустить приложение
```

---

## 🔄 Workflow для команды

### Первый запуск (новый разработчик)
```bash
git clone <repo>
cd python-clean-template
docker compose up
```

Готово! Всё работает.

### Обновление зависимостей
```bash
docker compose build
docker compose up
```

### Новая миграция
```bash
# создай SQL файл
docker compose exec app python -m src.infrastructure.database.migration_runner
```

---

Всё готово к работе! 🚀

