import pytest
import json
from app import app

def test_willsimms(): # creating card 30 is successful
    response = app.test_client().patch('/edit-card/30', json={
    "username": "willsimms",
    "title": "test edit title",
    "colour": "#fff",
    "content": "test edit content"
})
    assert response.status == '200 OK'

def test_no_username(): # error without username supplied
    response = app.test_client().patch('/edit-card/30', json={
    "title": "test edit title",
    "colour": "#fff",
    "content": "test edit content"
})
    assert response.status == '500 INTERNAL SERVER ERROR'




