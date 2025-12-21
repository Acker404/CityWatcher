from fastaapi import FastAPI
from fastaapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

origins = [
    "http://localhost:5173",  # Vite 預設 port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "backend is running"," message": "CityWeather API Ready"}

if __name__ == "__main__":
    uvicorn.run("app", host="0.0.0.0", port=8000)