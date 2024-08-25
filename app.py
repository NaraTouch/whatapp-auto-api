import uvicorn
from fastapi import FastAPI
from routes.main import router

app = FastAPI(
    title="WhatApp Automation API",
    description="This is Python rest api build for controller WhatApp Automation Users",
    version="1.0.0",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True
    }
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8181)