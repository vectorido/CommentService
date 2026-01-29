#!/bin/bash

HOST="${API_HOST:-http://localhost:8000}"

echo "🔥 API Examples"
echo "Host: $HOST"
echo ""
echo "💡 Tip: Install jq for pretty JSON output"
echo "   brew install jq  # macOS"
echo "   apt install jq   # Ubuntu"
echo ""

cat << 'EOF'
### Health Check
curl http://localhost:8000/health

### Create User
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","name":"John Doe"}'

### Get User
curl http://localhost:8000/users/1

### Get All Users
curl http://localhost:8000/users/

### Get Users with Pagination
curl "http://localhost:8000/users/?limit=10&offset=0"

### Update User
curl -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"John Updated"}'

### Delete User
curl -X DELETE http://localhost:8000/users/1

### With jq for pretty output
curl http://localhost:8000/users/ | jq .

### Save response to variable
USER_ID=$(curl -s -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test"}' | jq -r .id)
echo "Created user with ID: $USER_ID"

### HTTPie (more readable alternative to curl)
### Install: brew install httpie
http GET http://localhost:8000/users/
http POST http://localhost:8000/users/ email=test@example.com name="Test User"
http PUT http://localhost:8000/users/1 name="Updated Name"
http DELETE http://localhost:8000/users/1
EOF

