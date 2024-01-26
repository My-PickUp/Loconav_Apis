from __future__ import absolute_import
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from .routes import Vehicle_allocation, Customer_slots, Driver_slots
from .routes import device_latlon,add_fetch_data
from . import models
from .database import engine
 
app = FastAPI()

models.Base.metadata.create_all(bind = engine)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
                   )

@app.get("/")
def read_root():
    return {"Hello" : "World"}

app.include_router(device_latlon.router)
app.include_router(add_fetch_data.router)
#app.include_router(Driver_slots.router)

