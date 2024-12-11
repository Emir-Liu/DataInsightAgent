
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()


from config import SERVER_IP, SERVER_PORT, TITLE, VERSION
from router.solve import router as solve_router



print(f'environment:')
for key, value in os.environ.items():
    print(f'{key}: {value}')

app = FastAPI(title=TITLE, version=VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(solve_router)


if __name__ == '__main__':

    print(f'开始执行主程序')
    uvicorn.run(app, host=SERVER_IP, port=SERVER_PORT)
    