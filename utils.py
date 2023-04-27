from passlib.hash import pbkdf2_sha256

from config import Config

from mysql_connection import get_connection
from mysql.connector import Error



# 원문 비밀번호를, 암호화 하는 함수

def hash_password(original_password) :

    password=original_password + Config.SALT
    password=pbkdf2_sha256.hash(password)
    return password

# 유저가 로그인할 때 입력한 비밀번호가 맞는지 체크하는 함수
def check_password(original_password,hashed_password) :

    password=original_password + Config.SALT
    check = pbkdf2_sha256.verify(password,hashed_password)
    return check

def execute_query(query, params=None, fetch_all=True, dict_cursor=False):
    try:
        connection = get_connection()
        if dict_cursor:
            cursor = connection.cursor(dictionary=True)
        else:
            cursor = connection.cursor()

        cursor.execute(query, params)

        if "select" in query.lower():
            if fetch_all:
                result = cursor.fetchall()
            else:
                result = cursor.fetchone()
            return result
        else:
            connection.commit()

    except Error as e:
        print(e)
        raise e

    finally:
        cursor.close()
        connection.close()

def execute_select_query(query, record=None, dictionary=False):
    result_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=dictionary)

        if record:
            cursor.execute(query, record)
        else:
            cursor.execute(query)

        result_list = cursor.fetchall()
    except Error as e:
        print(e)
        raise
    finally:
        cursor.close()
        connection.close()

    return result_list

