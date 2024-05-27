import pandas as pd
from File_search import Files

LATTERS_TRANSKRIPTION = { # Перевод русских букв на похожие по форме английские если такое было
    "А": "A",
    "В": "B",
    "Е": "E",
    "К": "K",
    "М": "M",
    "Н": "H",
    "О": "O",
    "Р": "P",
    "С": "C",
    "Т": "T",
    "У": "Y",
    "Х": "X",
}

class DataBase:
    def __init__(self) -> None:
        self.base_path = "\\\PUBLIC\\Users\\Public-AGV\\Клиентская база\\Клиентская база с порядковыми номерами.xlsx"

    def find_client_number(self, client_name):
        try:
            database = pd.read_excel(self.base_path)
            for i in range(database.shape[0]):  # кол-во рядов
                if client_name.lower() in str(database["Клиент"][i]).lower():
                    # print(database["Клиент"][i], int(database["Идентификатор клиента"][i]))
                    return int(database["Идентификатор клиента"][i]), str(database["Клиент"][i])
        except Exception as error:
            print(error)

    def find_client_name(self, client_number):
        try:
            database = pd.read_excel(self.base_path)
            item = float(client_number)
            for i in range(database.shape[0]):
                if item == database["Идентификатор клиента"][i]:
                    # print(database["Клиент"][i], int(database["Идентификатор клиента"][i]))
                    return str(database["Клиент"][i])
        except Exception as error:
            print(error)

    def find_compressors(self, client_number: int):
        ''' Из базы берем список компрессоров конкретного клиента чтобы
        потом брать из маркера номер и искать название'''
        try:
            database = pd.read_excel(self.base_path)
            compressors = []  # a list of compressors of a specific client and their indeces in the database in a form of a tuple()
            item = float(client_number)
            for i in range(database.shape[0]):
                if item == database["Идентификатор клиента"][i]:
                    compressor_name = database["Установка/ступень"][i]
                    if "\n" in compressor_name:
                        compressor_name = " ".join(str(database["Установка/ступень"][i]).split("\n"))
                    compressor_index = int(database["Идентификатор установки"][i])
                    compressors.append((compressor_name, compressor_index))
            return compressors
        except Exception as error:
            print(error)

    def prind_db(self):
        database = pd.read_excel(self.base_path)
        print(database)


class Company:
    def __init__(self, company_number) -> None:
        self.data = DataBase()
        self.code = company_number
        self.company_name = self.data.find_client_name(self.code)
        self.compressors = self.data.find_compressors(self.code)

    @property
    def company_name(self):
        return self.__company_name

    @company_name.setter
    def company_name(self, value):
        self.__company_name = value


class Dereference_Marker:
    def __init__(self, full_name: str) -> None:
        self.full_name = full_name.strip()
        self.all_parameters = self.full_name.upper().strip("AGV ")
        self.nvk = self.get_nvk_num()
        self.kdpg = self.get_kdpg_num()
        self.diameter_num = self.get_diameter_num()
        self.company = Company(self.get_company_num())
        self.compressor = self.get_compressor_num()
        self.stage_num = self.get_stage_num()
        self.pressure = None

    def get_nvk_num(self):
        data = {1: "Нагнетательный", 2: "Всасывающий", 3: " Комбинированный", 4: "Обратный"}
        return data[int(self.all_parameters[0])]

    def get_kdpg_num(self):
        data = {1: "кольцевой", 2: "дисковый", 3: " пластинчатый", 4: "грибкового типа"}
        return data[int(self.all_parameters[1])]

    def get_diameter_num(self):
        try:
            with open(Files().file_diameters_path) as file:
                diameters = []
                diameter_index = ()
                for i in self.all_parameters:
                    char_index = self.all_parameters.index(i)
                    if i.isalpha() and self.all_parameters[char_index + 1].isalpha():
                        row = self.all_parameters[char_index: char_index + 2]
                        colomn = int(self.all_parameters[char_index + 2: -7])
                        if row in LATTERS_TRANSKRIPTION.keys():
                            row = LATTERS_TRANSKRIPTION[row]
                        diameter_index = (row, colomn)
                        break
                    if i.isalpha():
                        row = self.all_parameters[char_index]
                        column = ""
                        colomn = int(self.all_parameters[char_index + 1: -7])
                        if row in LATTERS_TRANSKRIPTION.keys():
                            row = LATTERS_TRANSKRIPTION[row]
                        diameter_index = (row, colomn)

                for i in file.readlines():
                    diameters.append(i.split())
                for i in diameters:
                    if diameter_index[0] in i[0]:
                        diameter_num = i[diameter_index[1]]
                        return int(diameter_num)
                else:
                    print("Нет доступного диаметра!")
        except Exception as error:
            print(error)

    def get_company_num(self):
        for i in self.all_parameters[::-1]:  # разворачиваем и ищем с конца букву
            return int(self.all_parameters[-7: -4])

    def get_compressor_num(self):
        for i in self.all_parameters:  # разворачиваем и ищем с конца букву
            if i == ".":
                index_char = self.all_parameters.index(i)
                compressor_num = int(self.all_parameters[index_char - 2:index_char])
                for i in self.company.compressors:
                    if int(i[1]) == compressor_num:
                        return i[0]

    def get_stage_num(self):
        for i in self.all_parameters:  # разворачиваем и ищем с конца букву
            if i == ".":
                index_char = self.all_parameters.index(i)
                return int(self.all_parameters[index_char + 1:])


def description():
    while True:
        mark = Dereference_Marker(input("Дай мне маркер: "))
        print(f"Тип клапана: {mark.nvk}")
        print(f"Вид клапана: {mark.kdpg}")
        print(f"Диаметр: {mark.diameter_num} мм")
        print(f"Компания: {mark.company.company_name}")
        print(f"Идентификационный номер компании: {mark.company.code}")
        print(f"Установка: {mark.compressor}")
        print(f"Ступень: {mark.stage_num}")
        if mark.nvk == "Нагнетательный":
            print()
            pressure = input(f"Какое давление нагнетания для {mark.compressor} {mark.stage_num} ступени: ")
            print()
            print("Описание клапана для PO")
            print(
                f"{mark.nvk} клапан d{mark.diameter_num} мм {mark.full_name} {mark.stage_num}-й ступени компрессора {mark.compressor}, давление нагнетания -  {pressure} кгс/см2, конечный заказчик - {mark.company.company_name}.")
            print()
        else:
            pressure = input(f"Какое давление всасывания для {mark.compressor} {mark.stage_num} ступени: ")
            print()
            print("Описание клапана для PO")
            print(
                f"{mark.nvk} клапан d{mark.diameter_num} мм {mark.full_name} {mark.stage_num}-й ступени компрессора {mark.compressor}, давление всасывания -  {pressure} кгс/см2, конечный заказчик - {mark.company.company_name}.")
            print()


def find_client():
    db = DataBase()
    print(numb := db.find_client_number(input("Введите имя клиента: ")))
    if numb is None:
        print("Нет клиента")
        return
    for compr in db.find_compressors(numb[0]):
        print(f"{compr[0]}, ид. номер {compr[1]}")


if __name__ == '__main__':
    while True:
        try:
            description()
        except Exception as error:
            print(error)
