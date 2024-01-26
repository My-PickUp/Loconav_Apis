from fastapi import FastAPI, APIRouter,Depends, HTTPException, Header
from sqlalchemy.orm import Session
from .. import models,schema
import requests
import json
from typing import List

router = APIRouter(
    prefix="/add_fetch_data",
    tags=['add_fetch_data']
)

user_auth = "aKUN3zzmW1X82jfNy6kw"

@router.get("/add_data_to_json/")
def put_data():
    payload = ""
    headers = {
    'User-Authentication': user_auth
    }

    url = "https://marketplace.loconav.com/api/v1/vehicles?page=1&per_page=&number=&fetch_motion_status=&fetch_odometer_reading=&fetch_mobilization_details="
    
    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.status_code)
    
    data = response.text
    
    data = json.loads(data)
    print(data)
    json_data = json.dumps(data, indent=2)
    
    file_path = "app/driver_Data_json.json"
    with open(file_path, "w") as json_file:
        json_file.write(json_data)
        
@router.get("/fetch_data_json/")
def fetch_data_json():
    file_path = "app/driver_Data_json.json"
    
    try:
        with open(file_path, "r") as read_file:
            data = json.load(read_file)
        return {"data": data}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Error decoding JSON: {str(e)}")
