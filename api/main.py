
from proc_model import runApp
import json
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

inv_hist = runApp()[0]
order_log = runApp()[1]
inv_history_json = json.loads(inv_hist.to_json(orient='records'))

@app.get("/")
async def root():
    return inv_history_json

@app.get("/proc_type/{proc_type}")
async def filter_proc(proc_type:str):
    k = inv_hist[inv_hist['surg_type']== proc_type]
    return json.loads(k.to_json(orient='records'))

@app.get("/order_log/{proc_type}")
async def filter_proc(proc_type:str):
    k = order_log[order_log['surg_type']== proc_type]
    return json.loads(k.to_json(orient='records'))
    

