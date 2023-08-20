import socket
import json
from ClassServer import DataServer as Database
import data_eng as de


data_dict = de.load_data_from_csv("train.csv")
server_instance = Database(data_dict)



HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8192         # The port used by the server
BUFFER_SIZE = 1024

request_send_row = {
    "action": "row",
    "data": "data"
}


def server_socket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        while True:  # Бесконечный цикл для прослушивания
            print('Listening for client...')
            conn, addr = s.accept()
            print('Connection address:', addr)
            try:
                data = conn.recv(BUFFER_SIZE).decode()
                request = json.loads(data)
                if "instruction" in request and request["instruction"]["action"] == "get_data":

                    offset = request["instruction"]["offset"]
                    limit = request["instruction"]["limit"]
                    response = server_instance.get_data_slice(offset, limit)
                    # Отправляем ответ частями
                    for i in response:
                        req = request_send_row
                        req["data"] = i
                        req = de.json_message(req)
                        req_binary = req.encode()  # Преобразуем строку в бинарный формат
                        conn.sendall(req_binary)
                        print("Строка отправлена")
                        
                    # Отправляем разделитель, чтобы указать конец ответа
                    conn.sendall(";".encode())
                    print("End of communication")    
                    conn.close()  # Закрываем соединение с клиентом
            except Exception as e:
                print("Error:", e)
                conn.close()  # В случае ошибки тоже закрываем соединение

server_socket()