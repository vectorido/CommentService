# Директория миграций

## Быстрый старт

### Создать новую миграцию
```bash
cat > src/infrastructure/database/migrations/002_create_products.sql << EOF
create table if not exists products (
    id serial primary key,
    name varchar(255) not null,
    price decimal(10, 2) not null
);
EOF
```

### Применить миграции
```bash
python -m src.infrastructure.database.migration_runner
```

### Проверить статус
```bash
python -m src.infrastructure.database.migration_runner status
```

## Правила именования

Формат: `{номер}_{описание}.sql`

Примеры:
- `001_create_users_table.sql`
- `002_create_products_table.sql`
- `003_add_user_avatar.sql`

**Важно:** Используй трёхзначные номера для правильной сортировки.

## Best Practices

1. ✅ Одна миграция = одно изменение
2. ✅ Используй `if not exists` для идемпотентности
3. ✅ Никогда не редактируй применённые миграции
4. ✅ Делай backup перед сложными миграциями

📖 Полное руководство: [docs/MIGRATIONS_GUIDE.md](../../../docs/MIGRATIONS_GUIDE.md)

