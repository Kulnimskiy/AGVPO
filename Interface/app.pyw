from tkinter import *
import sys
sys.path.insert(1,r"C:\Users\sk\Desktop\АГВ Проекты\PO_авто\V3")
import PO
from time import sleep


def finish():
    global the
    global closed
    closed = True
    lbl.configure(text="Покеда")
    print("Закрытие приложения")
    sleep(4)
    

main_window = Tk()
main_window.geometry("800x600")
main_window.resizable(False, False)
the = "Я тут все автоматизирую"
main_window.iconbitmap(default=r"C:\Users\sk\Desktop\АГВ Проекты\PO_авто\V3\Interface\icon.ico")
lbl = Label(main_window, text=the, font=("Arial Black", 35))
lbl.grid(column=0, row=0)
btn = Button(main_window, text="Сделай спецификацию",fg="black", bg="white", command= PO.main, font=("Arial Black", 25))
btn.grid(column=0, row=1)
main_window.title("AGV automation")
closed = False
main_window.protocol("WM_DELETE_WINDOW", finish)
if closed:
    main_window.destroy()  # ручное закрытие окна и всего приложения
mainloop()