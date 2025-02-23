from fastapi import APIRouter,Path,Query,Cookie,Header
from enum import Enum
from typing import Optional,List
from pydantic import BaseModel,Field
from DataHandingOfMySQL import get_words_rank,story_sentence1
from datetime import date

"""主要都是执行的是进行数据的存储----"""

app02 = APIRouter()

@app02.get("/search/phrase") #
def story_sentence(sentence: str ):
    if sentence:
        result = story_sentence1(sentence)
        response = {
            "code": 200,
            "msg": "数据返回成功",
            "data": {
                "data":result
            }
        }
    else:
        response = {
            "code": 400,
            "msg": "未提供有效的查询参数",
            "data": None
        }
    #下面去写一个sql语句，将这些内容都传输进去
    return  response
#这个是将bing的图片都保存下来
@app02.get("/story/picture") #添加参数
def story_picture(picture_data: str ):

    startdate=picture_data[0]['startdate']

    print("startdate",startdate)

    return {"message":"成功"}
#添加枚举,可以进行选择