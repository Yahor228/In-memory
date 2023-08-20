import json


class DataServer:
    def __init__(self, data_dict):
        self.data = {}  # Словарь для хранения данных по идентификатору
        self.sorted_data = list(data_dict.values())  # Список для сортированных данных

    def add_data(self, item):
        self.data[item["id"]] = item
        self.sorted_data.append(item)
        self.sorted_data.sort(key=lambda x: x["column1"])  # Сортировка по нужному столбцу
        self.notify_subscribers()

    def update_data(self, item):
        if item["id"] in self.data:
            self.data[item["id"]] = item
            for i, row in enumerate(self.sorted_data):
                if row["id"] == item["id"]:
                    self.sorted_data[i] = item
                    break
            self.sorted_data.sort(key=lambda x: x["column1"])  # Обновить сортировку
            self.notify_subscribers()

    def delete_data(self, item_id):
        if item_id in self.data:
            del self.data[item_id]
            self.sorted_data = [row for row in self.sorted_data if row["id"] != item_id]
            self.notify_subscribers()


    def get_data_slice(self, offset, N):
        if offset < 0 or offset >= len(self.sorted_data):
            return []  # Возвращаем пустой список, если offset некорректен

        end_index = offset + N
        data_slice = self.sorted_data[offset:end_index]

        # Добавляем ключ "Id" (с большой буквы) к каждому элементу в срезе
        data_slice_with_id = [{"Id": item["Id"], **item} for item in data_slice]

        return data_slice_with_id

   