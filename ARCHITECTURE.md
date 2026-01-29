# Архитектура проекта

## Принципы чистой архитектуры

Проект построен на принципах Clean Architecture (Robert Martin) и Domain-Driven Design (Eric Evans).

### Слои приложения

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│   (FastAPI routes, schemas, app)        │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│        Application Layer                │
│     (Use Cases, orchestration)          │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│          Domain Layer                   │
│  (Entities, Repository interfaces,      │
│   Domain Services, Exceptions)          │
└─────────────────▲───────────────────────┘
                  │
┌─────────────────┴───────────────────────┐
│      Infrastructure Layer               │
│  (DB connections, Repository impl,      │
│   External services)                    │
└─────────────────────────────────────────┘
```

### Правило зависимостей

Зависимости направлены **внутрь**:
- Infrastructure → Domain
- Application → Domain
- Presentation → Application → Domain

Domain слой **не зависит** ни от чего - это чистая бизнес-логика.

## Структура директорий

```
src/
├── domain/                     # Ядро приложения
│   ├── entities/              # Бизнес-сущности (User, Product, etc)
│   ├── repositories/          # Интерфейсы репозиториев (ABC)
│   ├── services/              # Доменные сервисы (бизнес-логика)
│   └── exceptions.py          # Доменные исключения
│
├── application/               # Бизнес-сценарии
│   └── use_cases/            # Use Cases (CreateUser, GetUser, etc)
│
├── infrastructure/            # Технические детали
│   ├── database/
│   │   ├── connection.py     # asyncpg connection pool
│   │   └── migrations.py     # SQL миграции
│   ├── repositories/         # Реализации репозиториев
│   │   └── postgres_user_repository.py
│   └── config.py             # Настройки приложения
│
└── presentation/              # Внешний интерфейс
    ├── api/
    │   ├── routes/           # FastAPI роутеры
    │   ├── dependencies.py   # DI контейнер
    │   └── app.py           # FastAPI приложение
    └── schemas/             # Pydantic схемы (DTO)
```

## Ключевые концепции

### 1. Entities (Сущности)

Бизнес-объекты с идентификатором и жизненным циклом:

```python
@dataclass
class User:
    id: Optional[int]
    email: str
    name: str
    created_at: Optional[datetime] = None
```

### 2. Repository Pattern

Интерфейс (в domain) + реализация (в infrastructure):

```python
class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

class PostgresUserRepository(UserRepository):
    async def get_by_id(self, user_id: int) -> Optional[User]:
        row = await self.db.fetchrow(...)
        return self._map_row_to_user(row)
```

### 3. Use Cases

Сценарии использования системы:

```python
class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(self, email: str, name: str) -> User:
```

### 4. Dependency Injection

Через FastAPI Depends:

```python
def get_user_repository():
    return PostgresUserRepository(db_connection)

@router.get("/{user_id}")
async def get_user(
    user_id: int,
    use_case: GetUserUseCase = Depends(get_get_user_use_case)
):
    return await use_case.execute(user_id)
```

## Почему asyncpg?

- ✅ Нативный async (не блокирует event loop)
- ✅ Максимальная производительность (в 3-5 раз быстрее psycopg2)
- ✅ Connection pool из коробки
- ✅ Автоматические prepared statements
- ✅ Стандарт для FastAPI приложений

## Почему без ORM?

1. **Контроль над SQL** - знаешь что именно выполняется
2. **Производительность** - нет overhead ORM
3. **Простота отладки** - видишь SQL напрямую
4. **Гибкость** - сложные запросы пишутся проще
5. **Чистая архитектура** - меньше magic, больше явности

## Добавление новой сущности

Пример: добавим сущность Product

### 1. Domain Layer

```python
# src/domain/entities/product.py
@dataclass
class Product:
    id: Optional[int]
    name: str
    price: Decimal

# src/domain/repositories/product_repository.py
class ProductRepository(ABC):
    @abstractmethod
    async def create(self, product: Product) -> Product:
        pass
```

### 2. Infrastructure Layer

```python
# src/infrastructure/repositories/postgres_product_repository.py
class PostgresProductRepository(ProductRepository):
    async def create(self, product: Product) -> Product:
        row = await self.db.fetchrow(
            "insert into products (name, price) values ($1, $2) returning *",
            product.name, product.price
        )
        return self._map_row_to_product(row)
```

### 3. Application Layer

```python
# src/application/use_cases/product_use_cases.py
class CreateProductUseCase:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    async def execute(self, name: str, price: Decimal) -> Product:
        product = Product(id=None, name=name, price=price)
        return await self.product_repository.create(product)
```

### 4. Presentation Layer

```python
# src/presentation/schemas/product_schemas.py
class ProductCreateRequest(BaseModel):
    name: str
    price: Decimal

# src/presentation/api/routes/products.py
@router.post("/")
async def create_product(
    request: ProductCreateRequest,
    use_case: CreateProductUseCase = Depends(...)
):
    return await use_case.execute(request.name, request.price)
```

## Тестирование

### Unit тесты (Use Cases)

```python
@pytest.mark.asyncio
async def test_create_user_use_case():
    mock_repo = Mock(spec=UserRepository)
    use_case = CreateUserUseCase(mock_repo)
    
    await use_case.execute("test@example.com", "Test User")
    
    mock_repo.create.assert_called_once()
```

### Integration тесты (API)

```python
@pytest.mark.asyncio
async def test_create_user_api(client: AsyncClient):
    response = await client.post("/users/", json={
        "email": "test@example.com",
        "name": "Test User"
    })
    assert response.status_code == 201
```

## Лучшие практики

1. **Domain всегда чистый** - никаких импортов из infrastructure/presentation
2. **Один Use Case = один сценарий** - не смешивайте логику
3. **Repository = коллекция** - думайте о нём как о списке в памяти
4. **Явные зависимости** - через конструктор, не глобальные переменные
5. **DTO на границах** - Pydantic схемы для API, domain entities внутри
6. **Типизация везде** - используйте type hints

## Полезные ссылки

- [Clean Architecture - Robert Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design - Eric Evans](https://www.domainlanguage.com/ddd/)
- [asyncpg documentation](https://magicstack.github.io/asyncpg/)
- [FastAPI documentation](https://fastapi.tiangolo.com/)

