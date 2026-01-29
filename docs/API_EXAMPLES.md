# API Examples

## 🚀 Способы тестирования API

### 1. REST Client (VS Code) - Самый удобный! ⭐

Установи [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) для VS Code.

Открой файл `api.http` и кликай кнопку **"Send Request"** над каждым запросом.

```bash
code api.http
```

Преимущества:
- ✅ Клик мышкой - запрос выполнен
- ✅ Видишь результаты прямо в редакторе
- ✅ История запросов
- ✅ Переменные окружения

---

### 2. Автоматический тест-скрипт

Запустит все эндпоинты последовательно:

```bash
chmod +x scripts/test_api.sh
./scripts/test_api.sh
```

Требования: `jq` для форматирования JSON
```bash
brew install jq  # macOS
apt install jq   # Ubuntu
```

---

### 3. curl команды

```bash
# Health Check
curl http://localhost:8000/health

# Создать пользователя
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","name":"John Doe"}'

# Получить пользователя
curl http://localhost:8000/users/1

# Получить всех пользователей
curl http://localhost:8000/users/

# С форматированием через jq
curl http://localhost:8000/users/ | jq .

# Обновить пользователя
curl -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"John Updated"}'

# Удалить пользователя
curl -X DELETE http://localhost:8000/users/1
```

Больше примеров в файле: `scripts/curl_examples.sh`

---

### 4. HTTPie (более читаемая альтернатива curl)

Установка:
```bash
brew install httpie  # macOS
apt install httpie   # Ubuntu
pip install httpie   # любая ОС
```

Использование:
```bash
# GET запрос
http GET http://localhost:8000/users/

# POST запрос (проще чем curl!)
http POST http://localhost:8000/users/ email=john@example.com name="John Doe"

# PUT запрос
http PUT http://localhost:8000/users/1 name="Updated Name"

# DELETE запрос
http DELETE http://localhost:8000/users/1
```

---

### 5. Swagger UI (встроен в FastAPI)

Открой в браузере: http://localhost:8000/docs

- ✅ Визуальный интерфейс
- ✅ "Try it out" кнопка для каждого эндпоинта
- ✅ Автоматическая документация
- ✅ Примеры запросов/ответов

---

### 6. Python requests

```python
import requests

BASE_URL = "http://localhost:8000"

response = requests.post(
    f"{BASE_URL}/users/",
    json={"email": "test@example.com", "name": "Test User"}
)
print(response.json())

user_id = response.json()["id"]

response = requests.get(f"{BASE_URL}/users/{user_id}")
print(response.json())
```

---

### 7. Docker (если используешь Docker)

```bash
# Запусти из контейнера
docker compose exec app curl http://localhost:8000/users/

# Или с хоста
curl http://localhost:8000/users/
```

---

## 📋 Примеры запросов

### Health Check
```bash
curl http://localhost:8000/health
```

Ответ:
```json
{"status":"ok"}
```

---

### Создать пользователя
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "name": "John Doe"
  }'
```

Ответ:
```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "name": "John Doe",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

---

### Получить пользователя
```bash
curl http://localhost:8000/users/1
```

---

### Получить всех пользователей
```bash
curl http://localhost:8000/users/
```

С пагинацией:
```bash
curl "http://localhost:8000/users/?limit=10&offset=0"
```

---

### Обновить пользователя
```bash
curl -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "John Updated"}'
```

Можно обновлять частично:
```bash
# Только имя
curl -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "New Name"}'

# Только email
curl -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"email": "new@example.com"}'

# Оба поля
curl -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"email": "new@example.com", "name": "New Name"}'
```

---

### Удалить пользователя
```bash
curl -X DELETE http://localhost:8000/users/1
```

---

## ❌ Примеры ошибок

### 404 - Пользователь не найден
```bash
curl http://localhost:8000/users/999
```

Ответ:
```json
{
  "detail": "User with id 999 not found"
}
```

---

### 409 - Дубликат email
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email": "existing@example.com", "name": "Test"}'
```

Ответ:
```json
{
  "detail": "User with email existing@example.com already exists"
}
```

---

### 422 - Невалидные данные
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email": "not-an-email", "name": "Test"}'
```

Ответ:
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address"
    }
  ]
}
```

---

## 🎯 Рекомендации

**Для разработки:** REST Client в VS Code (`api.http`)  
**Для автоматизации:** Скрипт `test_api.sh`  
**Для документации:** Swagger UI (http://localhost:8000/docs)  
**Для интерактивной работы:** HTTPie  
**Для CI/CD:** curl в скриптах  

---

## 💡 Полезные советы

### Сохранить ID из ответа
```bash
USER_ID=$(curl -s -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test"}' | jq -r .id)

echo "Created user: $USER_ID"
curl http://localhost:8000/users/$USER_ID
```

### Цикл создания пользователей
```bash
for i in {1..5}; do
  curl -X POST http://localhost:8000/users/ \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"user$i@example.com\",\"name\":\"User $i\"}"
done
```

### Тестирование производительности
```bash
# Apache Bench
ab -n 1000 -c 10 http://localhost:8000/users/

# wrk
wrk -t4 -c100 -d30s http://localhost:8000/users/
```

---

Готово! Выбирай любой удобный способ! 🚀

