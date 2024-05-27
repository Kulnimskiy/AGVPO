import time


class Compressor:
    '''Класс собирает характеристики компрессора чтобы по ним составить его маркеровку'''

    def __init__(self) -> None:
        self.first_num = self.get_first_num()
        self.second_num = self.get_second_num()
        self.diameter = self.get_diameter_marker()
        self.unit_number = self.get_unit_number()  # Номер компрессора
        self.stage_number = self.get_stage_number()  # Номер ступени в этом компрессоре

    # Первую строчку в файле не берем. Она с индексами. Ее по факту вообще можно убрать, но пусть будет чтобы другим было понятно
    def get_diameter_marker(self):
        while True:
            with open("C:\\Users\\User\\Desktop\\AGV projects\\Автоматическая маркировка\\Посадочный размер в мм.txt", "r", encoding="utf-8") as file:
                diameter = input("Какой посадочный диаметр?: ").strip().lower()
                for i in file.readlines()[1:]:
                    indeces = i.split()
                    if str(diameter) in indeces:
                        return str(indeces[0]).strip(". ") + str(indeces.index(str(diameter)))
                else:
                    print("Нет такого в списке. Попробуйте еще раз")

    # Пока все на интупе. По идее нужно делать список отдельно и чтобы программа сама из него брала нужную информацию
    def get_first_num(self):
        while True:
            types = ["н", "в", "к", "о"]
            type_of_compressor = input(
                "Тип клапана(н = нагнетательный, в = всасывающий,к = комбинированный, о = обратный): ").strip().lower()
            for i in types:
                if i == type_of_compressor:
                    return str(types.index(i) + 1)
            else:
                print("Компрессор не найден. Попробуйте еще раз")

    def get_second_num(self):
        while True:
            types = ["к", "д", "п", "гт"]
            type_of_compressor = input(
                "Тип клапана(к = кольцевой, д = дисковый,п = пластинчатый, гт = грибкового типа): ").strip().lower()
            for i in types:
                if i == type_of_compressor:
                    return str(types.index(i) + 1)
            else:
                print("Компрессор не найден. Попробуйте еще раз")

    def get_unit_number(self):
        while True:
            num = input("Введите номер установки?: ").strip().lower()
            if len(num) < 3 and num.isdigit():
                return num.rjust(2, "0")
            else:
                print("Неправильный нормер установки. Введите еще раз")

    def get_stage_number(self):
        while True:
            num = input("Введите номер ступени?: ").strip().lower()
            if len(num) < 3 and num.isdigit():
                return f".{num}"
            else:
                print("Неправильный нормер установки. Введите еще раз")


class Client(Compressor):
    def __init__(self) -> None:
        self.company_name = input("Имя компании: ")
        self.id_number = self.get_client_num()
        self.markers = []

    def get_client_num(self):
        while True:
            num = input("Введите номер клиента в базе?: ").strip().lower()
            if len(num) == 3:
                return num
            elif len(num) < 3 and num != 0:
                return num.rjust(3, "0")
            else:
                print("Неправильный номер. Введите заново")

    def add_markers(self):
        print(f"Добавляем номенкулатуру клиенту {self.company_name}")
        item = Compressor()
        marker = f"AGV{item.first_num}{item.second_num}{item.diameter}{self.id_number}{item.unit_number}{item.stage_number}"
        print(marker)
        self.markers.append(marker)


def create_company():
    novotech = Client()
    while True:
        answer = input(f"Добавить маркеры в компанию {novotech.company_name}?(Enter если да / любое другое если нет): ")
        if answer.lower().strip() == "":
            novotech.add_markers()
            print('\n')
        else:
            print(f"Вы добавили {len(novotech.markers)} макреров для компании {novotech.company_name}")
            with open(
                    f"C:\\Users\\User\\Desktop\\AGV projects\\Автоматическая маркировка\\Маркировки\\{novotech.company_name} маркеровки.txt",
                    "a", encoding="utf-8") as f:
                for i in novotech.markers:
                    f.write(str(i) + '\n')
                    print(i)
            print(f"Все записано в файле '{novotech.company_name} маркеровки.txt'")
            time.sleep(15)
            break


def main():
    try:
        create_company()
    except FileNotFoundError as error:
        print(error)
        print("Маркеров не было создано")
        main()


if __name__ == '__main__':
    main()
