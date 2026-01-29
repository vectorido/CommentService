#!/bin/bash

set -e

HOST="${API_HOST:-http://localhost:8000}"

echo "🧪 Testing API at $HOST"
echo "================================"
echo ""

echo "📍 1. Health Check"
curl -s "$HOST/health" | jq .
echo -e "\n"

echo "📍 2. Create User - John Doe"
USER1=$(curl -s -X POST "$HOST/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"john.doe@example.com","name":"John Doe"}' | jq .)
echo "$USER1"
USER1_ID=$(echo "$USER1" | jq -r .id)
echo -e "\n"

echo "📍 3. Create User - Jane Smith"
USER2=$(curl -s -X POST "$HOST/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"jane.smith@example.com","name":"Jane Smith"}' | jq .)
echo "$USER2"
USER2_ID=$(echo "$USER2" | jq -r .id)
echo -e "\n"

echo "📍 4. Get User by ID: $USER1_ID"
curl -s "$HOST/users/$USER1_ID" | jq .
echo -e "\n"

echo "📍 5. Get All Users"
curl -s "$HOST/users/" | jq .
echo -e "\n"

echo "📍 6. Update User: $USER1_ID"
curl -s -X PUT "$HOST/users/$USER1_ID" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Updated"}' | jq .
echo -e "\n"

echo "📍 7. Get Updated User: $USER1_ID"
curl -s "$HOST/users/$USER1_ID" | jq .
echo -e "\n"

echo "📍 8. Try to create duplicate email (should fail with 409)"
curl -s -X POST "$HOST/users/" \
  -H "Content-Type: application/json" \
  -d '{"email":"jane.smith@example.com","name":"Another Jane"}' | jq .
echo -e "\n"

echo "📍 9. Try to get non-existent user (should fail with 404)"
curl -s "$HOST/users/999" | jq .
echo -e "\n"

echo "📍 10. Delete User: $USER1_ID"
curl -s -X DELETE "$HOST/users/$USER1_ID"
echo "User deleted"
echo -e "\n"

echo "📍 11. Verify deletion (should fail with 404)"
curl -s "$HOST/users/$USER1_ID" | jq .
echo -e "\n"

echo "✅ All tests completed!"

