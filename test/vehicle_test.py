from http import HTTPStatus
import pytest

def test_success_get_vehicle_by(client):
    vin = "2HGFA16538H523456"
    response = client.get(f"/lookup/{vin}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'vin': '2HGFA16538H523456',
        'make': 'HONDA',
        'model_year': '2008',
        'model': 'Civic',
        'body_class': 'Sedan/Saloon',
        'cached_result': False
    }
    
    response = client.get(f"/lookup/{vin}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'vin': '2HGFA16538H523456',
        'make': 'HONDA',
        'model_year': '2008',
        'model': 'Civic',
        'body_class': 'Sedan/Saloon',
        'cached_result': True
    }

def test_failure_get_vehicle_by_wrong_vin(client):
    vin = "WRONGVIN"
    response = client.get(f"/lookup/{vin}")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    
def test_failure_get_vehicle_by_none_vin(client):
    vin = None
    response = client.get(f"/lookup/{vin}")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    
def test_success_delete_vehicle_by_vin(client):
    vin = "5N1AT2ML1FC830078"
    response_get = client.get(f"/lookup/{vin}")
    assert response_get.status_code == HTTPStatus.OK
    
    response_delete = client.delete(f"/remove/{vin}")
    assert response_delete.status_code == HTTPStatus.OK
    assert response_delete.json() == {'vin':'5N1AT2ML1FC830078',
                                    'cached_delete_success':True}
                            
def test_failure_delete_vehicle_by_wrong_vin(client):
    vin = "TESTWRONGVIN12345"
    response = client.delete(f"/remove/{vin}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'vin':'TESTWRONGVIN12345',
                                'cached_delete_success':False}
    
def test_failure_delete_vehicle_by_short_vin(client):
    vin = "SHORTWRONGVIN"
    response = client.delete(f"/remove/{vin}")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    
def test_failure_delete_vehicle_by_none_vin(client):
    vin = None
    response = client.delete(f"/remove/{vin}")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    
def test_success_export_database_cache_bytes(client):
    with client.websocket_connect("/export") as websocket:
        assert websocket.receive_bytes() != None
        
def test_failure_export_database_cache_json(client):
    with pytest.raises(Exception):
        with client.websocket_connect("/export") as websocket:
            assert websocket.receive_json() != None
        
def test_failure_export_database_cache_text(client):
    with pytest.raises(Exception):
        with client.websocket_connect("/export") as websocket:
            assert websocket.receive_text() != None