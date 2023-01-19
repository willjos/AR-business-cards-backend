import pytest
import json
from app import app

def test_willsimms(): # creating card is successful
    response = app.test_client().post('/create-card', json={
    "username": "willsimms",
    "title": "test title",
    "colour": "#fff",
    "content": "test content"
})
    assert response.status == '200 OK'

def test_no_username(): #no username supplied request fails
    response = app.test_client().post('/create-card', json={
    "title": "test title",
    "colour": "#fff",
    "content": "test content"
})
    assert response.status == '500 INTERNAL SERVER ERROR'

def test_no_card_data(): #no username supplied request fails
    response = app.test_client().post('/create-card', json={
    "username": "willsimms"
})
    assert response.status == '500 INTERNAL SERVER ERROR'