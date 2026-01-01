from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import os
from dotenv import load_dotenv

load_dotenv()

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
# TDX API 設定
def get_auth_token():
    token_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id':os.getenv('TDX_CLIENT_ID'),
        'client_secret': os.getenv('TDX_CLIENT_SECRET')
    }
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()

        token_info = response.json()
        access_token = token_info.get("access_token")
        print("Success TDX Token!")
        return access_token
    except Exception as e:
        print(f"Error fetching token: {e}")
        return None
def get_livie_city_cameras(city = "Taipei"):
    token = get_auth_token()
    if not token:
        return {"error": "Failed to get TDX token"}

    url = f"https://tdx.transportdata.tw/api/basic/v2/Road/Traffic/CCTV/City/{city}"
    headers = {"authorization": f"Bearer {token}"}
    params = {
        "$top" : 20,
        "$format": "JSON"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching live city cameras: {e}")
        return {"error": "Failed to fetch live city cameras"}
@app.get("/")
def read_root():
    token = get_auth_token()
    if token:
        return {"status": "backend is running","tdx_auth": "success"}
    else:
        return {"status": "backend is running","tdx_auth": "failed"}
@app.get("/api/cameras")
def get_cameras_endpoint():
    cameras = get_livie_city_cameras("Taipei")
    return cameras

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)