

import csv
import socket
import json
from socket import error as SocketError
import errno

BUFFER_SIZE = 1024

def load_data_from_csv(csv_file):
    data_dict = {}
    
    with open(csv_file, "r") as file:
        csv_reader = csv.reader(file)
        
        # Получение заголовков (первая строка)
        headers = next(csv_reader)
        column_indices = {header: index for index, header in enumerate(headers)}
        
        for row in csv_reader:
            item_id = row[0]
            item_values = {}

            for i in range(len(row)):
                if i == 0:
                    item_values[headers[i]] = row[i]  # Сохраняем первое значение как строку (id)
                else:
                    try:
                        item_values[headers[i]] = int(row[i])  # Попытка преобразования в целое число
                    except ValueError:
                        item_values[headers[i]] = row[i]  # Если не удалось, сохраняем как строку

            if item_id not in data_dict:
                data_dict[item_id] = item_values
            else:
                data_dict[item_id].update(item_values)

    return data_dict


def json_message(direction):
    local_ip = socket.gethostbyname(socket.gethostname())
    data = {
        'sender': local_ip,
        'instruction': direction
    }

    json_data = json.dumps(data, sort_keys=False, indent=2)

    print(json_data)
    return json_data




def get_data_client(data, HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data.encode())

        req = ""
        while True:
            try:
                chunk = s.recv(BUFFER_SIZE).decode()
                req += chunk
                if req[-1] == ";":
                    s.close()
                    return req
            except SocketError as e:
                if e.errno != errno.ECONNRESET:
                    raise
                pass

    