from openpyxl import Workbook
from tkinter import Tk
from tkinter.filedialog import askopenfilename,askdirectory
from Read_specification import Specification

def main():
    po = Workbook()
    ws = po.active
    header = [["","","","Наименование","ИНН/КПП"],
            ["","","Покупатель","АГВ"],
            ["","","Продавец","ТРЭМ-Инжиниринг"],
            ["","","Конечный покупатель","____(вставить)___"],
            ["","","Контактное лицо",""],
            ["","","Номер контракта"],
            ["","","PO No"],
            ["","","Способ отгрузки","автотранспорт"],
            ["","","Номер ценового предложения"],
            ["","","Дата заказа"],
            ["","","Запрошенная дата отгрузки"],
            ["","","Подтвержденная дата отгрузки"],
            ["","","Условия поставки", "Склад Заказчика"],
            ["№", "Описание", "Артикул","Номер чертежа", "№ сборки", "Наименование АГВ для отгрузки Конечнику","Кол-во, шт", "Цена, за шт, руб без НДС", "Всего, руб без НДС","ФИО Подготовил/Проверил"]]
    for row in header:
        ws.append(row)

    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename(title="Выберите спецификацию")  # show an "Open" dialog box and return the path to the selected file
    spec = Specification(filename)
    try:
        raw_counter = 0
        worker_name = input("Ты кто?: ").strip().title()
        for i in spec._items:
            if i is None:
                raw_counter += 1
                description = "Не знаю еще"
                article = ""
                drawings_num = ""
                assembling_num = ""
                name_agv = spec.items_name_quant[raw_counter-1][0]
                quantity = spec.items_name_quant[raw_counter-1][1]
                cost_one = ""
                cost_all = ""
                ws.append([raw_counter, description, article, drawings_num, assembling_num, name_agv, quantity, cost_one, cost_all, worker_name])
            else:
                raw_counter += 1
                description = i.description
                article = ""
                drawings_num = ""
                assembling_num = ""
                name_agv = spec.items_name_quant[raw_counter - 1][0]
                quantity = spec.items_name_quant[raw_counter - 1][1]
                cost_one = i.cost
                cost_all = cost_one * int(quantity)
                ws.append([raw_counter,description ,"","","",name_agv, quantity, cost_one, cost_all ,worker_name])
    except Exception as error:
        print(error)
    destination_dir = askdirectory(title="Куда сохранить PO")
    po.save(f"{destination_dir}\PO.xlsx")

if __name__ == "__main__":
    main()