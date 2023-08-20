import socket
import json
import data_eng as de
# from requests import request_get 
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8192         # The port used by the server

BUFFER_SIZE = 1024  # Размер буфера

request_get = {
    "action": "get_data",
    "offset": 0,
    "limit": 50,
    "sort_column": "column1",
    "sort_order": "asc"
}





while True:
    a = int(input("1. обновить данные , 2 получить окно данных: "))
    if a == 2:
        offset = int(input("Введите индекс начала фрейма: "))
        request_get["offset"] = offset
        limit =  int(input("Введите размер фрэйма:"))
        request_get["limit"] = limit 
        jsonObj = de.json_message(request_get)
        req = de.get_data_client(jsonObj,HOST,PORT)
        print(req)
