from dbutils.pooled_db import PooledDB
import pymysql

pool = PooledDB(
    creator=pymysql,  # 使用 pymysql 作为数据库连接库
    maxconnections=10,  # 连接池大小为 10
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    database='beibeiword',
    charset='utf8mb4'
)
conn = pool.connection()
cursor = conn.cursor()


def get_words_db(word):
    select_query = '''
    SELECT * FROM words WHERE word = %s
    '''
    account_update_query = '''
    UPDATE words SET account = account + 1 WHERE word = %s
    '''
    cursor.execute(select_query, (word,))
    result = cursor.fetchone()

    cursor.execute(account_update_query, (word,))
    if (result):
        resultData = result
    else:
        resultData = "抱歉请更新您的词库"
    conn.commit()
    return resultData


# 去执行数据库中的单词排行榜，从高到低进行排行
def get_words_rank():
    select_query = '''
    SELECT * FROM words order by account  DESC LIMIT 100;
    '''
    cursor.execute(select_query)
    return cursor.fetchall()


# 储存句子
def story_sentence1(data):
    select_story = '''
   INSERT INTO sentence (phrase, account) VALUES (%s, %s)
    '''
    cursor.execute(select_story, (data, 1))
    conn.commit()
    response = {
        "message": "数据插入成功"
    }
    return response


# 去执行记单词的功能
def get_recite_words(id: int):
    sql = '''SELECT * FROM words WHERE id >= %s ORDER BY id LIMIT 25;'''
    cursor.execute(sql, (id,))
    result = cursor.fetchall()
    return result


# 去将单词挑战的人员显示出来
def get_change_rank():
    sql = '''
    SELECT  * FROM changegame ORDER BY maxdata DESC LIMIT 5
    '''
    cursor.execute(sql)
    return cursor.fetchall()


# 给背的单词去增加 1
def add_recite_words(id: int):
    sql = '''UPDATE  words SET recited = recited + 1 WHERE id = %s; '''
    cursor.execute(sql, (id,))
    conn.commit()
    return "错误单词的数量增加了 1 "


# 给错误的值去增加 1
def add_wrong_words(id: int):
    sql = '''UPDATE  words SET wrongtime = wrongtime + 1 WHERE id = %s; '''
    cursor.execute(sql, (id,))
    conn.commit()
    return "错误单词的数量增加了 1 "


# 去获取随机的一个单词然后显示其完成的单词
def get_guss_word(id: int):
    sql = '''SELECT * FROM words WHERE id = %s'''
    cursor.execute(sql, (id,))
    result = cursor.fetchone()
    return result


# 关闭数据库连接
def close_connection():
    cursor.close()
    conn.close()
