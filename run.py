import uvicorn
from fastapi import FastAPI
from function import app04,app02,app03
app = FastAPI()

app.include_router(app03,prefix='/Part1', tags=['Part1的操作部分'])
app.include_router(app02,prefix='/Part2', tags=['Part2的操作部分'])
app.include_router(app04,prefix='/Part3', tags=['Part3的操作部分'])

if __name__ == '__main__':
    uvicorn.run('run:app',host='0.0.0.0',port=8000,reload=True,  workers=1)
