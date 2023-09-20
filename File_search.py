import os

class Files:
    def __init__(self) -> None:
        self.cur_dir = os.path.dirname(os.path.realpath(__file__))
        self.file_diameters_name = "Посадочный размер в мм.txt"
        self.file_cost_name = "СебестоимостьТРЭМ-АГВ+Прайс расчет (калькулятор).xlsx"
        self.file_diameters_path = self.find(self.file_diameters_name, self.cur_dir)
        self.file_cost_path = self.find(self.file_cost_name, self.cur_dir)

    def find(self, name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
            
    
def verification():
    while not Files().file_cost_path:
        input(f"Нет файла {Files().file_cost_name} в папке c программы или он назван не так. Перенесите или переименуйте и нажмине Enter: ")
    while not Files().file_diameters_path:
        input(f"Нет файла {Files().file_diameters_name} в папке c программы или он назван не так. Перенесите или переименуйте и нажмине Enter: ")

verification()

def test():
    while True:
        print(Files().file_cost_path)
        print(Files().file_diameters_path)
        input()

if __name__ == "__main__":
    test()
