# 4moshe

Run:
python sanicapp.py

Usage example:

Authorization:
curl -iv -H "Content-Type: application/json" -d '{"username": "user1", "password": "123456"}' http://localhost:16001/auth

Normalization:
curl -iv -H "Authorization: Bearer <JWT from reply>" -H 'Content-Type: application/json' -d '[{"name": "device","strVal": "iPhone", "metadata": "not interesting"},{ "name": "isAuthorized", "boolVal": "false","lastSeen": "not interesting"}]' http://localhost:16001/normalize
