from tkinter import *
import sys
sys.path.insert(1,r"C:\Users\sk\Desktop\АГВ Проекты\PO_авто\V3")
import PO
import Template
from time import sleep


main_window = Tk()
main_window.geometry("450x350")
main_window.resizable(False, False)
C = Canvas(main_window, bg="blue", height=350, width=450)
# filename = PhotoImage(file=r"C:\\Users\\sk\\Desktop\\АГВ Проекты\\PO_авто\\V3\\Interface\\main_background.jpg")
# background_label = Label(main_window, image=filename)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)
C.pack()
the = "Я ТУТ ВСЕ АВТОМАТИЗИРУЮ"
main_window.iconbitmap(default=r"C:\Users\sk\Desktop\АГВ Проекты\PO_авто\V3\Interface\icon.ico")
lbl = Label(main_window, text=the, font=("Arial Black", 15),bg="white")
lbl.place(x=15, y=10)
btn_spec = Button(main_window, text="Сделай \nспецификацию",fg="black", bg="white", command= PO.main, font=("Arial Black", 15))
btn_spec.place(x=10, y=80)
btn_templ = Button(main_window, text="Сделай \nШаблон",fg="black", bg="white", command= Template.main, font=("Arial Black", 15))
btn_templ.place(x=250, y=80)
btn_create_mark = Button(main_window, text="Создай Маркер",fg="black", bg="white", command= PO.main, font=("Arial Black", 15))
btn_create_mark.place(x=10, y=180)
btn_info = Button(main_window, text="Info",fg="black", bg="white", command= PO.main, font=("Arial Black", 15))
btn_info.place(x=270, y=180)
main_window.title("AGV automation")

mainloop()