import pytest
import json
from app import app

willsimms_firstQR = {
    "id": 9,
    "title": "TestEdit3"
  }

def test_willsimms(): # user willsimms returns 200 response, with correct expected data
    response = app.test_client().get('/getUserQR?username=willsimms')
    assert response.status == '200 OK'
    assert json.loads(response.data.decode('utf-8'))[0] == willsimms_firstQR

def test_nonUser(): # user notauser returns 404 response.
    response = app.test_client().get('/getUserQR?username=notauser')
    assert response.status == '404 NOT FOUND'
