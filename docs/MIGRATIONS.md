# Миграции - Краткая справка

## Команды

### Применить миграции
```bash
python -m src.infrastructure.database.migration_runner
```

### Проверить статус
```bash
python -m src.infrastructure.database.migration_runner status
```

---

## Добавить новую миграцию

### Шаг 1: Создай SQL файл
```bash
cat > src/infrastructure/database/migrations/002_create_products.sql << EOF
create table if not exists products (
    id serial primary key,
    name varchar(255) not null,
    price decimal(10, 2) not null,
    created_at timestamp default current_timestamp
);

create index idx_products_name on products(name);
EOF
```

### Шаг 2: Примени
```bash
python -m src.infrastructure.database.migration_runner
```

---

## Частые примеры

### Создать таблицу
```sql
create table if not exists orders (
    id serial primary key,
    user_id integer references users(id) on delete cascade,
    total_amount decimal(10, 2) not null
);
```

### Добавить колонку
```sql
alter table users add column if not exists phone varchar(20);
```

### Создать индекс
```sql
create index if not exists idx_users_phone on users(phone);
```

---

## Best Practices

1. ✅ Формат: `{номер}_{описание}.sql` (001, 002, 003)
2. ✅ Используй `if not exists` / `if exists`
3. ✅ Одна миграция = одно изменение
4. ✅ Не редактируй применённые миграции

---

📖 Полное руководство: [docs/MIGRATIONS_GUIDE.md](docs/MIGRATIONS_GUIDE.md)

