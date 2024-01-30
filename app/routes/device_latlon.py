from fastapi import FastAPI, APIRouter,Depends, HTTPException, Header
from sqlalchemy.orm import Session
from .. import models,schema
import requests
import json
from typing import List

router = APIRouter(
    prefix="/Customer_slots",
    tags=['Customer_slots']
)

def return_data():
    file_path = "app/driver_Data_json.json"
    with open(file_path, "r") as read_file:
            data = json.load(read_file)
    return data

def get_serial_number(data,phone : str):
    for entry in data['data']:
        if "device" in entry and "phone_number" in entry["device"]:
            if entry["device"]["phone_number"] == phone:
                serial_number = entry["device"]["serial_number"]
                print(serial_number)
                return(serial_number)
            
def get_serial_number_vhnumber(data, vhnumber : str):
    for entry in data['data']:
        if "display_number" in entry:
            if entry["display_number"][:10] == vhnumber:
                serial_number = entry["device"]["serial_number"]
                print(serial_number)
                return(serial_number)

user_auth = "aKUN3zzmW1X82jfNy6kw"

url1 = "https://marketplace.loconav.com/api/v1/maps/eta"

def get_eta_func(source_lat_lon : List[float], dest_lat_lon : List[float]):
    print(source_lat_lon)
    print(dest_lat_lon)

    
    payload = json.dumps({
    "sources": source_lat_lon,
    "destinations": dest_lat_lon
    })
    headers = {
    'User-Authentication': user_auth,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url1, headers=headers, data=payload)
    
    print("Response status code:", response.status_code)
    print("Response content:", response.text)
    
    return(response.text)

@router.post('post_get_eta')
def get_eta(source_lat_lon : List[float], dest_lat_lon : List[float]):
    print(source_lat_lon)
    print(dest_lat_lon)
    
    source_ar = [str(",".join([str(i) for i in source_lat_lon]))]
    dest_ar = [str(",".join([str(i) for i in dest_lat_lon]))]
    
    print(source_ar)
    print(dest_ar)
    
    payload = json.dumps({
    "sources": source_ar,
    "destinations": dest_ar
    })
    headers = {
    'User-Authentication': user_auth,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url1, headers=headers, data=payload)
    
    print("Response status code:", response.status_code)
    print("Response content:", response.text)


@router.get("/estimated_time/")
def estimated_time(
    phone_number : str = Header(..., description="User's phone number"),
    lat : str = Header(..., description='User lat'),
    lon : str = Header(..., description='User lon')
    ):
    
    data = return_data()
    
    serial_number = get_serial_number(data,phone_number)

    print(serial_number)

    if serial_number is None:
        return {"phone_number is not valid"}
        
    url = f'https://marketplace.loconav.com/api/v1/devices/lookup?serial_number={serial_number}'
    headers = {
     'User-Id': '2526220',
    'Admin-Authentication': '_G4q_g5nZ5gxDKTWQhN_'
    }

    response = requests.request("GET", url, headers=headers)

    location_data = response.text
    
    location_data = json.loads(location_data)
    
    location = location_data["data"]["device_info"]["location"]
    
    print(location)
    
    source_latlon = [location]
    dest_latlon = [str(lat) + "," + str(lon)]
    
    eta = get_eta_func(source_lat_lon = source_latlon, dest_lat_lon = dest_latlon)
    
    eta= json.dumps(json.loads(eta))
        
    return eta

@router.get("/estimated_time_vh_number/")
def estimated_time_vh(
    vehicle_number : str = Header(..., description="Driver's Vehicle number"),
    lat : str = Header(..., description='User lat'),
    lon : str = Header(..., description='User lon')
    ):
    
    data = return_data()
    
    serial_number = get_serial_number_vhnumber(data,vehicle_number)
        
    url = f'https://marketplace.loconav.com/api/v1/devices/lookup?serial_number={serial_number}'

    headers = {
     'User-Id': '2526220',
    'Admin-Authentication': '_G4q_g5nZ5gxDKTWQhN_'
    }

    response = requests.request("GET", url, headers=headers)

    location_data = response.text
    
    location_data = json.loads(location_data)

    print(location_data)
        
    if location_data is None:
        return {"there is no data"}
    
    location = location_data["data"]["device_info"]["location"]
    
    print(location)
    
    source_latlon = [location]
    dest_latlon = [str(lat) + "," + str(lon)]
    
    eta = get_eta_func(source_lat_lon = source_latlon, dest_lat_lon = dest_latlon)
    
    eta= json.dumps(json.loads(eta))
        
    return eta
