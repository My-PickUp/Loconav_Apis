from fastapi import FastAPI, APIRouter,Depends, HTTPException, Header
from ..database import get_db,engine
from sqlalchemy.orm import Session
from .. import models,schema
import requests
import json
from typing import List

models.Base.metadata.create_all(bind = engine)

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
        
    url = 'https://marketplace.loconav.com/api/v1/devices/lookup?serial_number=0867440060507290'
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