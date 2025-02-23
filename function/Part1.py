from fastapi import APIRouter, Path, Query, Cookie, Header
from enum import Enum
import pprint

from random import sample, random, randint
from typing import Optional, List
from pydantic import BaseModel, Field
from ConnectionPoolDB import get_words_db, get_words_rank, get_recite_words, add_wrong_words, add_recite_words, \
    get_change_rank, get_guss_word
from datetime import date

app03 = APIRouter()

"""主要执行的是数据的查询"""

"""关于单词的数据的查询部分"""


@app03.get("/search/query")  # 没有参数
def query_words(data: str = Query(None)):
    result = get_words_db(data)
    if is_alphabet(result[1]):
        response = {
            "code": 200,
            "msg": "数据返回成功",
            "data": {
                "id": result[0],
                "word": result[1],
                "pronounce": result[2],
                "type": result[3],
                "explain": result[4],
                "exampleSentence": result[5],
                "exampleSentenceChinese": result[6]
            }
        }
    else:
        response = {
            "code": 400,
            "msg": "未提供有效的查询参数",
            "data": None
        }

    return response


"""单词的排行榜"""


@app03.get("/search/all")  # 没有参数
def query_rank_words():
    results = get_words_rank()
    formatted_results = []
    rank = 1
    for result in results:
        formatted_result = {
            "rank": rank,
            "account": result[7],
            "id": result[0],
            "word": result[1],
            "pronounce": result[2],
            "type": result[3],
            "explain": result[4],
            "exampleSentence": result[5],
            "exampleSentenceChinese": result[6]
        }
        formatted_results.append(formatted_result)
        rank += 1
    return formatted_results


"""在此执行记单词的功能"""


@app03.get("/recite/getwords")
def get_words_remember(word_id: int = 100, model: int = 1):
    """如果是 1 则执行的是按顺序- 2则是乱序"""
    wrongData = []
    word_data_story = []
    formatted_results = []
    data = sample(range(26), 3)
    if model == 1:
        modelData = "模式1"
        results = get_recite_words(word_id)  # 以25为例，你可以传入任何你想要的ID值
    else:
        modelData = "模式2"
        randomData = randint(10, 10000)  # 获取随机值
        results = get_recite_words(randomData)
    for result in results:
        formatted_result = {
            "id": result[0],
            "word": result[1],
            "pronounce": result[2],
            "type": result[3],
            "explain": result[4],
            "exampleSentence": result[5],
            "exampleSentenceChinese": result[6]
        }
        formatted_results.append(formatted_result)

    for result in formatted_results:
        wrong_result = {
            "id": result['id'],
            "word": result['word'],
            "pronounce": result['pronounce'],
            "type": result['type'],
            "explain": result['explain'],
        }
        wrongData.append(wrong_result)
    for i in range(3):
        word_data_story.append(wrongData[data[i]])
    # 将正确的结果和错误的结果都进行随机的打乱然后去传输过去
    formatted_results = [formatted_results[0]]
    word_data_story = [word_data_story[0], word_data_story[1], word_data_story[2]]

    data_list = [formatted_results[0], *word_data_story]

    random_list = sample(data_list, len(data_list))

    response = {
        "code": 200,
        "msg": "哦吼,数据返回成功喽~",
        "model": modelData,
        "right": formatted_results,
        "data": random_list
    }
    return response


"""将背的单词的量增 1"""


@app03.get("/search/recite")
def add_recite_times(id: int):
    result = add_recite_words(id)
    response = {
        "code": 200,
        "msg": "哦吼,数据返回成功喽~",
        "data": result
    }
    return response


"""如果是错误的单词要记得增加 1"""


@app03.get("/search/wrong")
def add_wrong_times(id: int):
    result = add_wrong_words(id)
    response = {
        "code": 200,
        "msg": "哦吼,数据返回成功喽~",
        "data": result
    }
    return response


"""挑战背单词的功能"""


@app03.get("/search/change")
def query_rank_words():
    results = get_change_rank()
    formatted_results = []
    rank = 1
    for result in results:
        formatted_result = {
            "rank": rank,
            "id": result[0],
            "maxdata": result[1],
            "accountvalue": result[2],
            "username": result[3],
            "userid": result[4],
            "faildword": result[5],
            'image': result[6]
        }
        formatted_results.append(formatted_result)
        rank += 1
    return formatted_results


"""缺词小游戏-model具有三关，难度系数不一样"""
@app03.get("/search/gussWord")
def query_get_guss_word(model: int):
    global result
    randomData = randint(10, 10000)  # 获取随机值
    toGetWords = get_guss_word(randomData)
    if model == 1:
        if len(toGetWords[1]) not in range(1, 4):
            query_get_guss_word(model=1)
        else:
            result = dataFormate(data=toGetWords,model=model)

    elif model == 2:
        if len(toGetWords[1]) not in range(4, 7):
            query_get_guss_word(model=2)
        else:
            result = dataFormate(data=toGetWords, model=model)

    elif model == 3:

        if len(toGetWords[1]) not in range(7, 20):
            query_get_guss_word(model=3)
        else:
            result = dataFormate(data=toGetWords,model=model)

    response = {
        "code": 200,
        "msg": "哦吼,数据返回成功喽~",
        "data": result
    }
    return response


# 难度关卡1,2,3 通过模式来进行字母的减少
def challengeDifficulty(word, model):
    indices = sample(range(0, len(word) - 1), model * 2 - 1)
    randomized_word = list(word)
    for index in indices:
        randomized_word[index] = '_'
    return ''.join(randomized_word)


# 难度关卡同时减少单词解释的意思也就是减少提示量
def reduceTips(explain, model):
    global result
    # 则进行分割以分号来进行分割
    explainList = explain.split(';')
    if model == 1:
        return explainList
    elif model == 2:
        return explainList[:len(explainList) // 2]
    elif model == 3:
        return explainList[0]

#进行数据格式化，增强代码复用性
def dataFormate(data,model):
    result = {
        "type": data[3],
        "resultWord": data[1],
        "pronunciation": data[2],
        "explain": reduceTips(data[4], model=model),
        "missingWords": challengeDifficulty(word=data[1], model=model)
    }
    return result
# p判断是不是单词
def is_alphabet(char):
    return 'a' <= char <= 'z' or 'A' <= char <= 'Z'


def is_chinese(char):
    return '\u4e00' <= char <= '\u9fff'






class CityName(str, Enum):
    Beijing = "Beijing China"
    Shanghai = "Shanghai China"


@app03.get("/enum/{city}")
async def laters(city: CityName):
    if city == CityName.Shanghai:
        return {"city_name": city, "confirm": 12345}
    if city == CityName.Beijing:
        return {"city_name": city, "confirm": "unknow numbers"}


# 来进行文件的路径的校验
@app03.get("/files/{file_path:path}")  # 通过path parameters传递文件路径
def filepath(file_path: str):
    return f"The file path is {file_path}"


@app03.get("/path_/{num}")
def path_params_validate(
        num: int = Path(..., title="Your Number", description="不可描述", ge=1, le=10),
):
    return num


# 参数的查询和字符串的验证
@app03.get("/query")  # 可以去用来查询数量的设置
def page_limit(page: int = 1, limit: Optional[int] = None):
    if limit:
        return {"page": page, "limit": limit}
    return {"page": page}


@app03.get("/query/bool/conversion")  # 可以去用来查询数量的设置
def type_conversion(param: bool = False):
    return param


@app03.get("/query/validations")  # 长度+正则表达式验证，比如长度8-16位，以a开头。其它校验方法看Query类的源码
def query_params_validate(
        value: str = Query(..., min_length=2, max_length=16, regex="^a"),  # ...换成None就变成选填的参数
        values: List[str] = Query(["v1", "v2"], alias="alias_name")
):  # 多个查询参数的列表。参数别名
    return value, values


"""Request Body and Fields 请求体和字段"""


class CityInfo(BaseModel):
    name: str = Field(..., example="Beijing")  # example是注解的作用，值不会被验证
    country: str
    country_code: str = None  # 给一个默认值
    country_population: int = Field(default=800, title="人口数量", description="国家的人口数量", ge=800)

    class Config:
        schema_extra = {
            "example": {
                "name": "Shanghai",
                "country": "China",
                "country_code": "CN",
                "country_population": 140000,
            }
        }


@app03.post("/request_body/city")
def city_info(city: CityInfo):
    print(city.name, city.country)  # 当在IDE中输入city.的时候，属性会自动弹出
    return city.model_dump()


"""Request Body + Path parameters + Query parameters 多参数混合"""


@app03.put("/request_body/city/{name}")
def mix_city_info(
        name: str,
        city01: CityInfo,
        city02: CityInfo,  # Body可以是多个的
        confirmed: int = Query(ge=0, description="确诊数", default=0),
        death: int = Query(ge=0, description="死亡数", default=0),
):
    if name == "Shanghai":
        return {"Shanghai": {"confirmed": confirmed, "death": death}}
    return city01.model_dump(), city02.model_dump()


# 来进行数据的嵌套的使用
class Data(BaseModel):
    city: List[CityInfo]
    date: date
    confirmed: int = Field(ge=0, description="确诊人数", default=0)
    deaths: int = Field(ge=0, description="死亡人数", default=0)
    recovered: int = Field(ge=0, description="痊愈人数", default=0)


@app03.put("request_body/nested")
def nested_models(data: Data):
    return data


"""Cookie 和 Header 参数"""


@app03.get("/cookie")  # 效果只能用Postman测试
def cookie(cookie_id: Optional[str] = Cookie(None)):  # 定义Cookie参数需要使用Cookie类，否则就是查询参数
    return {"cookie_id": cookie_id}


@app03.get("/header")
def header(user_agent: Optional[str] = Header(None, convert_underscores=True), x_token: List[str] = Header(None)):
    """
    有些HTTP代理和服务器是不允许在请求头中带有下划线的，所以Header提供convert_underscores属性让设置
    :param user_agent: convert_underscores=True 会把 user_agent 变成 user-agent
    :param x_token: x_token是包含多个值的列表
    :return:
    """
    return {"User-Agent": user_agent, "x_token": x_token}
