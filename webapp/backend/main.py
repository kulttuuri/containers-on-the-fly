# Main entrypoint for the whole app

# TODO: Required?
#from importlib import reload
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes.api import router as api_router
from settings import settings

app = FastAPI()

# Setup allowed origins
origins = [settings.app["url"] + ":" + str(settings.app["port"])]

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add all routes
app.include_router(api_router)

# Start the app
if __name__ == '__main__':
    uvicorn.run("main:app", host=settings.app["host"], port=int(settings.app["port"]), log_level="info", reload=True)
    print("running")