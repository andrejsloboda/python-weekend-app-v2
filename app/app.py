import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.router import v1_api_router

# Init FastAPI
app = FastAPI()

# API configuration for front-end
origins = ["*"]
app.add_middleware( 
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["GET"],
    allow_headers=["application/json"]
)

app.include_router(v1_api_router)

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, log_level="info")




    








  







    

    
    
    
    
    
    
    
