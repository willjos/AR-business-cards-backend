import pytest
import json
from app import app

def test_willsimms_collection(): 
    response = app.test_client().post("/view-collection", json={"username": "willsimms"})
    assert response.status == '200 OK'
    assert json.loads(response.data.decode('utf-8'))[0]["id"] == 6