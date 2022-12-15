from http import HTTPStatus
import pytest
import pytest
import pandas as pd

def test_success_get_vehicle_by(client):
    valid_vin = "2HGFA16538H523456"
    
    # Look up data that's from vPic API, hence cached_result = False
    response = client.get(f"/lookup/{valid_vin}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'vin': '2HGFA16538H523456',
        'make': 'HONDA',
        'model_year': '2008',
        'model': 'Civic',
        'body_class': 'Sedan/Saloon',
        'cached_result': False
    }
    
    # Since the above call already inserted the data, now when it calls the same route with the same VIN
    # it fetches the data from the database, hence cached_result = True
    
    response = client.get(f"/lookup/{valid_vin}")
    
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
    invalid_vin = "WRONGVIN"
    response = client.get(f"/lookup/{invalid_vin}")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    
def test_failure_get_vehicle_by_none_vin(client):
    invalid_vin = None
    response = client.get(f"/lookup/{invalid_vin}")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
   
def test_failure_invalid_get_vehicle_by_vin(client):
    
    # To make sure the route works only with get request
    valid_vin = "2HGFA16538H523456"
    
    response = client.put(f"/lookup/{valid_vin}")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    
    response = client.post(f"/lookup/{valid_vin}")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    
    response = client.delete(f"/lookup/{valid_vin}")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    
    
def test_success_delete_vehicle_by_vin(client):
    valid_vin = "5N1AT2ML1FC830078"
    response_get = client.get(f"/lookup/{valid_vin}")
    assert response_get.status_code == HTTPStatus.OK
    
    response_delete = client.delete(f"/remove/{valid_vin}")
    assert response_delete.status_code == HTTPStatus.OK
    assert response_delete.json() == {'vin':'5N1AT2ML1FC830078',
                                    'cached_delete_success':True}
                            
def test_failure_delete_vehicle_by_wrong_vin(client):
    invalid_vin = "TESTWRONGVIN12345"
    response = client.delete(f"/remove/{invalid_vin}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'vin':'TESTWRONGVIN12345',
                                'cached_delete_success':False}
    
def test_failure_delete_vehicle_by_short_vin(client):
    invalid_vin = "SHORTWRONGVIN"
    response = client.delete(f"/remove/{invalid_vin}")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    
def test_failure_delete_vehicle_by_none_vin(client):
    invalid_vin = None
    response = client.delete(f"/remove/{invalid_vin}")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

def test_failure_invalid_delete_vehicle_by_vin(client):
    
    # To make sure the route works only with delete request
    valid_vin = "2HGFA16538H523456"
    
    response = client.put(f"/remove/{valid_vin}")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    
    response = client.post(f"/remove/{valid_vin}")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    
    response = client.get(f"/remove/{valid_vin}")
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

def test_success_empty_export_database_cache_bytes(client):
    with client.websocket_connect("/export") as websocket:
        parquet_binary_file = websocket.receive_bytes()
        parquet_decoded_file = pd.read_parquet(parquet_binary_file)
        
        # Since 0 valid_vids have been inserted, 
        # the length of values written in parquet file should also be 0
        assert parquet_decoded_file.empty == True
        assert len(parquet_decoded_file.values) == 0
        
def test_success_single_export_database_cache_bytes(client):
    valid_vin = "1G2ZA5EK1A4132890"
    
    response = client.get(f"/lookup/{valid_vin}")
    assert response.status_code == HTTPStatus.OK
    
    with client.websocket_connect("/export") as websocket:
        parquet_binary_file = websocket.receive_bytes()
        parquet_decoded_file = pd.read_parquet(parquet_binary_file)
        
        # Since 1 valid_vids have been inserted, 
        # the length of values written in parquet file should also be 1
        assert parquet_decoded_file.empty == False
        assert len(parquet_decoded_file.values) == 1
        
def test_success_multiple_export_database_cache_bytes(client):
    valid_vins = ["2HGFA16538H523456", "1B4GP44G1WB509825", "1G2ZA5EK1A4132890"]
    
    for valid_vin in valid_vins:
        response = client.get(f"/lookup/{valid_vin}")
        assert response.status_code == HTTPStatus.OK
    
    with client.websocket_connect("/export") as websocket:
        parquet_binary_file = websocket.receive_bytes()
        parquet_decoded_file = pd.read_parquet(parquet_binary_file)
        
        # Since 3 valid_vids have been inserted, 
        # the length of values written in parquet file should also be 3
        assert parquet_decoded_file.empty == False
        assert len(parquet_decoded_file.values) == 3
        
def test_success_invalid_export_database_cache_bytes(client):
    invalid_vin = "TESTWRONGVIN12345"
    
    response = client.get(f"/lookup/{invalid_vin}")
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    
    with client.websocket_connect("/export") as websocket:
        parquet_binary_file = websocket.receive_bytes()
        parquet_decoded_file = pd.read_parquet(parquet_binary_file)
        
        # Since an invalid vin has been attempted and failed , 
        # parquet file should also be empty
        assert parquet_decoded_file.empty == True
        assert len(parquet_decoded_file.values) == 0
        
def test_failure_export_database_cache_json(client):
    with pytest.raises(Exception):
        with client.websocket_connect("/export") as websocket:
            
            # Since websocket sends data in bytes,
            # the attempt to receive it as json should fail
            assert websocket.receive_json() != None
        
def test_failure_export_database_cache_text(client):
    with pytest.raises(Exception):
        with client.websocket_connect("/export") as websocket:
            
             # Since websocket sends data in bytes,
            # the attempt to receive it as text should fail
            assert websocket.receive_text() != None