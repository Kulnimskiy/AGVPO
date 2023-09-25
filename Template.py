import Read_specification
import openpyxl
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def main():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    tmplt = Template(filename)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Компрессор", "ступень", "Давление нагнетания", "Давление всавывания"])
    for compressor in Template.no_pressure_lst:
         comp = compressor[0]
         st = compressor[1]
         print(comp, st)
         ws.append([comp, st])
    wb.save("C:\\Users\\sk\\Desktop\\АГВ Проекты\\PO_авто\\V3\\tmpl.xlsx")
    pass

class Template(Read_specification.Specification):

    no_pressure_lst = [] #список компрессоров где не указано давление

    def __init__(self, spec_path=None) -> None:
        self.path = spec_path
        self.table = super().get_table_info()
        self.items_name_quant = super().get_items_name_quant()
        self.get_items()
        Template.no_pressure_lst = []

    def get_items(self):
        for specification_agv_name in self.items_name_quant:
            zip_valve_triggers = ["зип","ремонт"]
            if "клапан" in specification_agv_name[0].lower() and any(trigger in specification_agv_name[0].lower() for trigger in zip_valve_triggers):
                Read_specification.Specification._items.append(Zip_valve_Template(specification_agv_name[0]))
            elif "клапан" in specification_agv_name[0].lower() and all(trigger not in specification_agv_name[0].lower() for trigger in zip_valve_triggers):
                Read_specification.Specification._items.append(Valve_Template(specification_agv_name[0]))
            else:
                Read_specification.Specification._items.append(None)

class Valve_Template(Read_specification.Valve):
    def __init__(self, specification_agv_name):
        self.name = super()
        self.marker = super().get_marker(specification_agv_name)
        self.parameters = super().get_parameters()
        self.write_pressure()
        
    def write_pressure(self):
        item = (self.parameters.compressor, self.parameters.stage_num)
        if self.parameters.pressure is None and item not in Template.no_pressure_lst:
                self.parameters.pressure = "found"
                Template.no_pressure_lst.append((self.parameters.compressor, self.parameters.stage_num))


class Zip_valve_Template(Read_specification.ZipValve):
    def __init__(self, specification_agv_name):
        self.name = "зип клапана"
        self.marker = super().get_marker(specification_agv_name)
        self.parameters = super().get_parameters()
        self.write_pressure()
        
    def write_pressure(self):
        if self.parameters.pressure is None and self.parameters.compressor not in [i[0] for i in Template.no_pressure_lst]:
                self.parameters.pressure = "found"
                Template.no_pressure_lst.append((self.parameters.compressor, self.parameters.stage_num))

if __name__ == "__main__":
    main()
    print("Шаблон готов")