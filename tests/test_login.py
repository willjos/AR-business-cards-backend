import pytest
import json
from app import app

def test_willsimms_success(): # logging in as willsimms success with correct password
    response = app.test_client().post('/login', json={
    "username": "willsimms",
    "password": "test"
})
    assert response.status == '200 OK'

def test_willsimms_fail(): # logging in as willsimms fails with incorrect password
    response = app.test_client().post('/login', json={
    "username": "willsimms",
    "password": "incorrectpass"
})
    assert response.status == '403 FORBIDDEN'