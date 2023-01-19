import pytest
import json
from app import app

def test_register_success(): # success registering new user
    response = app.test_client().post('/register-user', json={
    "username": "newuser3", # note, usernames supplied must be unique so this will only work once
    "password": "test"
})
    assert response.status == '200 OK'

def test_register_fail(): # registering as willsimms fails as user already exists
    response = app.test_client().post('/register-user', json={
    "username": "willsimms",
    "password": "password"
})
    assert response.status == '500 INTERNAL SERVER ERROR'