from fastapi import FastAPI
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware
from user.router import user_router
from config import Settings
from utilities import *

import logging
from datetime import datetime
import tracemalloc
tracemalloc.start()
from fastapi import FastAPI, WebSocket
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

logging.basicConfig(level=logging.INFO)

app=FastAPI()
logger = logging.getLogger("FastAPI app")
setting =Settings()

app.include_router(user_router)

from fastapi import WebSocket






""" allows a server to indicate any origins (domain, scheme, or port) """
origins = ["*"]
app.add_middleware(CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )



# import requests

# # Define the endpoint and parameters
# ad_account_id = 'act_1392812424324321'
# url = f'https://graph.facebook.com/v13.0/{ad_account_id}/campaigns'
# params = {
#     'access_token': "EAAHfs7ej2kEBOyfzyOUWwEVJ8RKIm5eWWWN93aGNTyjM6vkWZA7avxCFFVfsSvyLUa7bmaz6qmLsh4Jlha4x6oWONZCf0QBIjTT0XFqZAnsvzunRFMf5nTrZCq3WNHZAVCk6hSeKDZBkjb0W03iPB5FvHY06t9zPJJVIKSg4M1sVQeGPT7RkuVCPvuqE4LJVT0kuUETQFHn7k84I2RoKWHgaJrdLd03CvZC3nbJlwIM4ktlsFiSpZAxe",
#     'fields': 'id,name,status,objective,created_time,updated_time'
# }

# # Make a request to the Meta Ads API
# response = requests.get(url, params=params)

# # Parse the response
# if response.status_code == 200:
#     print(response.json().get(""))
#     campaigns = response.json().get('data', [])
#     print('Campaigns:', campaigns)
# else:
#     print('Error fetching campaigns:', response.status_code, response.text)



@app.websocket("/")
async def stream_response(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text wa eees: {data}")
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
    except Exception as e:
        await websocket.send_text(f"An error occurred: {str(e)}")
    finally:
        await websocket.close()



# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     try:
#         await websocket.accept()
#         while True:
#             data = await websocket.receive_text()
#             await websocket.send_text(f"Message text was: {data}")
#     except Exception as ex:
#         return {"message": f"{str(ex)}"}
    
if __name__ == '__main__':
    uvicorn.run(app="main:app",host="0.0.0.0",port=setting.MAIN_PORT,reload=True)