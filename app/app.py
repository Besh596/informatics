from fastapi import FastAPI
from pydantic import BaseModel
import threading

class CountUpdate(BaseModel):
    value: int

app = FastAPI()
count = 0
lock = threading.Lock()
total_visits = 0
reset_count = 0

def atomic_inc_reset():
    global reset_count
    with lock:
        reset_count +=1

def atomic_inc_total():
    global total_visits
    with lock:
        total_visits +=1

def atomic_inc_count():
    global count 
    with lock:
        count += 1

@app.get("/counter/visit")
def counter_visit():
    atomic_inc_count()
    atomic_inc_total()
    return {"count": count, "message": "string"}

@app.get("/counter/current")
def counter_current():
    return {"count": count}

@app.get("/counter/reset")
def counter_reset():
    atomic_inc_reset()
    count = 0
    return {"count": count, "message": "reset"}

@app.get("/counter/stats")
def counter_stats():
    return {"total_visits": total_visits, "reset_count": reset_count}

@app.post("/counter/set")
def counter_set(update: CountUpdate):
    count = update.value
    return {"count": count, "message": "updated"}


