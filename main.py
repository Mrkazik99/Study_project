from fastapi import FastAPI, status, responses
from fastapi.middleware.cors import CORSMiddleware
import db

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return responses.JSONResponse(status_code=status.HTTP_201_CREATED, content={'message': 'Hello world!'})

@app.get("/input")
async def input():
    db.insert_employee('mat', 'mat', 'mat')
    return responses.Response(status_code=status.HTTP_201_CREATED)

@app.get("/get")
async def get():
    res = db.get_employee()
    print(res)
    print(res.show())
    return responses.JSONResponse(status_code=status.HTTP_200_OK, content={'workers': res})

