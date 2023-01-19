import pytest
import json
from app import app

card_6_response = {
    "colour": "#FF69B4",
    "content": "Test 1",
    "id": 6,
    "title": "Will Test 1",
    "user_id": 22
}

def test_willsimms(): # viewing card 6 is successful
    response = app.test_client().post('/view-card/6', json={"username": "willsimms"})
    assert response.status == '200 OK'
    assert json.loads(response.data.decode('utf-8'))[0] == card_6_response

def test_no_username(): # no username supplied is successful
    response = app.test_client().post('/view-card/6', json={"username": ""})
    assert response.status == '200 OK'
    assert json.loads(response.data.decode('utf-8'))[0] == card_6_response

def test_non_user(): # non-existent user is successful
    response = app.test_client().post('/view-card/6', json={"username": "notauser"})
    assert response.status == '200 OK'
    assert json.loads(response.data.decode('utf-8'))[0] == card_6_response

def test_non_card(): # non-existent card is successful (returns [])
    response = app.test_client().post('/view-card/10000', json={"username": "willsimms"})
    assert response.status == '200 OK'
    assert not json.loads(response.data.decode('utf-8'))

def test_bad_request(): # no username key sent in body fails.
    response = app.test_client().post('/view-card/6', json={"notusername": "willsimms"})
    assert response.status == '500 INTERNAL SERVER ERROR'