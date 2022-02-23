# GUI Library
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


def check_bill():
    global change
    try:
        if len(Payment_Amount_Entry.get()) == 0:
            messagebox.showerror("ข้อผิดพลาด", "กรุณากรอกจำนวนเงิน", parent=window)
        else:
            income = int(Payment_Amount_Entry.get())
            if final_price > income:
                messagebox.showerror("จำนวนเงินไม่ถูกต้อง", "เงินไม่พอจ่าย", parent=window)
            else:
                change = income - final_price
                Change_Label.config(text="เงินทอน {} บาท".format(change))
                messagebox.showinfo("สำเร็จ", "เงินทอน {} บาท".format(change), parent=window)

    except ValueError:
        messagebox.showerror("ข้อผิดพลาด", "จำนวนเงินไม่ถูกต้อง", parent=window)
    except TypeError:
        messagebox.showerror("ข้อผิดพลาด", "จำนวนเงินไม่ถูกต้อง", parent=window)


def set_option_member(selected):
    if selected != 0:
        MemberNumberEntry.configure(state=NORMAL)
    else:
        MemberNumberEntry.configure(state=DISABLED)
        
        
def set_option_discount(selected):
    if selected != 0:
        DiscountCodeEntry.configure(state=NORMAL)
        if selected == 1:
            cal_discount(total_price, 5)
        elif selected == 2:
            cal_discount(total_price, 10)
        elif selected == 3:
            cal_discount(total_price, 15)
        elif selected == 4:
            cal_discount(total_price, 20)
        cal_final_price()
    else:
        cal_discount(total_price, 0)
        DiscountCodeEntry.configure(state=DISABLED)


def cal_discount(base_price, discount_percentage):
    global total_discount
    total_discount = (discount_percentage / 100) * base_price
    Total_Discount_Label.config(text="ลดราคา {} บาท".format(total_discount))


def cal_final_price():
    global final_price
    final_price = total_price - total_discount
    Final_Price_Label.config(text="ราคาที่ต้องจ่ายปัจจุบัน {} บาท".format(final_price))


def cal_total_price():
    global total_price
    for key, val in menu_entry_list.items():
        if key in default_price and menu_entry_list[key] != 0:
            total_price += default_price[key] * val


def total_price_reset():  # in case user press "ทำรายการ" and close the window without do anything
    global total_price
    total_price = 0
    final_price = 0
    window.destroy()


def start_cal():
    cal_total_price()
    global window, MemberNumberEntry, DiscountCodeEntry, Menulist, Total_Discount_Label, Final_Price_Label, Payment_Amount_Entry, Change_Label
    window = Toplevel()
    window.title("{} - ทำรายการ".format(restaurant_name))
    window.resizable(FALSE, FALSE)
    window.geometry("%dx%d+0+0" % (width, height))
    window.grab_set()

    TopListLabel = Label(window, text="รายการอาหาร", fg=color_red, bg=color_yellow, width=23)
    TopListLabel.grid(row=0, column=0, sticky=W)
    TopMemberLabel = Label(window, text="บัตรสมาชิก/บัตรส่วนลด", fg=color_yellow, bg=color_red, width=30)
    TopMemberLabel.grid(row=0, column=1, sticky=W)

    Menulist = Text(window, width=23, height=10)
    Menulist.configure(state=DISABLED)
    Menulist.grid(row=1, column=0, sticky=W)
    copy_menu()

    Total_Price_Label = Label(window, text="ราคารวมทุกรายการ {} บาท".format(total_price))
    Total_Price_Label.grid(row=1, column=0)
    Total_Price_Label.place(x=0, y=360)

    Total_Discount_Label = Label(window, text="ลดราคา {} บาท".format(0))
    Total_Discount_Label.grid(row=1, column=0)
    Total_Discount_Label.place(x=0, y=400)

    Final_Price_Label = Label(window, text="ราคาที่ต้องจ่ายปัจจุบัน {} บาท".format(0))
    Final_Price_Label.place(x=0, y=440)
    cal_final_price()

    Change_Label = Label(window, text="เงินทอน {} บาท".format(0))
    Change_Label.place(x=0, y=480)

    MemberNumberLabel = Label(window, text="บัตรสมาชิก")
    MemberNumberLabel.grid(row=1, column=1, sticky=NW)

    MemberStringVar = StringVar()
    MemberNumberCombobox = ttk.Combobox(window, textvariable=MemberStringVar)
    MemberNumberCombobox["values"] = ("ไม่มีหมายเลขสมาชิก", "มีหมายเลขสมาชิก")
    MemberNumberCombobox["state"] = "readonly"
    MemberNumberCombobox.bind("<<ComboboxSelected>>", lambda _: set_option_member(MemberNumberCombobox.current()))
    MemberNumberCombobox.current(0)
    MemberNumberCombobox.grid(row=1, column=1, sticky=NE)

    MemberNumberEntryLabel = Label(window, text="ระบุเลขสมาชิก")
    MemberNumberEntryLabel.place(x=445, y=85)
    MemberNumberEntry = Entry(window)
    MemberNumberEntry.place(x=619, y=85, width=400)
    MemberNumberEntry.configure(state=DISABLED)

    DiscountCodeLabel = Label(window, text="ส่วนลด")
    DiscountCodeLabel.grid(row=2, column=1, sticky=NW)
    DiscountCodeLabel.place(x=445, y=135)
    DiscountVar = StringVar()
    DiscountCombobox = ttk.Combobox(window, textvariable=DiscountVar)
    DiscountCombobox["values"] = ("ไม่มีส่วนลด", "5%", "10%", "15%", "20%")
    DiscountCombobox["state"] = "readonly"
    DiscountCombobox.bind("<<ComboboxSelected>>", lambda _: set_option_discount(DiscountCombobox.current()))
    DiscountCombobox.current(0)
    DiscountCombobox.grid(row=2, column=1, sticky=NW)
    DiscountCombobox.place(x=619, y=135)

    DiscountLabel = Label(window, text="ระบุรหัสส่วนลด")
    DiscountLabel.grid(row=3, column=1, sticky=NW)
    DiscountLabel.place(x=445, y=175)

    DiscountCodeEntry = Entry(window)
    DiscountCodeEntry.place(x=619, y=175, width=400)
    DiscountCodeEntry.configure(state=DISABLED)

    OperateLabel = Label(window, text="การชำระเงิน", fg=color_yellow, bg=color_blue)
    OperateLabel.grid(row=4, column=1)
    OperateLabel.place(x=445, y=215, width=575)

    Payment_Amount_Label = Label(window, text="ช่องทางการชำระเงิน")
    Payment_Amount_Label.grid(row=5, column=1)
    Payment_Amount_Label.place(x=445, y=255)

    Payment_Method_Var = StringVar()
    Payment_Method_Combobox = ttk.Combobox(window, textvariable=Payment_Method_Var)
    Payment_Method_Combobox["values"] = ("เงินสด", "พร้อมเพย์", "โอนเงินธนาคาร")
    Payment_Method_Combobox["state"] = "readonly"
    Payment_Method_Combobox.current(0)
    Payment_Method_Combobox.bind("<<ComboboxSelected>>", lambda _: ...)
    Payment_Method_Combobox.grid(row=7, column=2)
    Payment_Method_Combobox.place(x=690, y=255, width=325)

    Payment_Method_Label = Label(window, text="ป้อนจำนวนเงิน")
    Payment_Method_Label.grid(row=6, column=2)
    Payment_Method_Label.place(x=445, y=295)

    Payment_Amount_Entry = Entry(window)
    Payment_Amount_Entry.grid(row=5, column=2)
    Payment_Amount_Entry.place(x=690, y=295, width=325)

    ConfirmButton = Button(window, text="ยืนยันการชำระเงิน", fg=color_green, command=check_bill)
    ConfirmButton.place(x=445, y=360, width=575)

    CancelBillBotton = Button(window, text="ยกเลิกรายการ", fg=color_red, command=window.destroy)
    CancelBillBotton.place(x=445, y=420, width=575)

    window.protocol("WM_DELETE_WINDOW", total_price_reset)
    window.mainloop()


def cancel_menu():
    global menu_entry_list, total_price
    for key in menu_entry_list:
        menu_entry_list[key] = 0
    total_price = 0
    MenuListLabel.configure(state=NORMAL)
    MenuListLabel.delete(0.0, END)
    MenuListLabel.insert(0.0, "กรุณาเลือกเมนูอาหารทางด้านซ้ายมือ")
    MenuListLabel.configure(state=DISABLED)


def copy_menu():
    Menulist.configure(state=NORMAL)
    for key, val in menu_entry_list.items():
        if val == 0:
            pass
        else:
            if key in default_price:
                text = "{} x {} คิดเป็น{}บาท{}".format(key, val, default_price[key] * val, "\n")
                Menulist.insert(0.0, text)


def add_menu(menu):
    if menu in menu_entry_list:
        menu_entry_list[menu] += 1
        MenuListLabel.configure(state=NORMAL)
        MenuListLabel.delete(0.0, END)
        for key, val in menu_entry_list.items():
            if val == 0:
                pass
            else:
                if key in default_price:
                    text = "{} x {} คิดเป็น{}บาท{}".format(key, val, default_price[key] * val, "\n")
                    MenuListLabel.insert(0.0, text)
        MenuListLabel.configure(state=DISABLED)

    else:
        print("Error, No Menu in Dict")


# Variable Declaration
menu_entry_list = {"Salmon": 0, "Spaghetti": 0, "Burger": 0, "Soup": 0, "Pizza": 0, "French Fired": 0,
                   "Hot Dog": 0, "Steak": 0, "Salad": 0}

default_price = {"Salmon": 200, "Spaghetti": 100, "Burger": 80, "Soup": 80, "Pizza": 100, "French Fired": 80,
                 "Hot Dog": 50, "Steak": 120, "Salad": 70}
total_price = 0
total_discount = 0
final_price = 0
change = 0
# Font
font_name = "PSL-omyim"
font_size_label = 20
font_size_button = 16
font_style_bold = "bold"

restaurant_name = "Nuu Imm Cafe"
title = "{} - โปรแกรมคิดเงิน".format(restaurant_name)

# Color
color_red = "red"
color_yellow = "yellow"
color_pink = "pink"
color_gold = "gold"
color_black = "black"
color_green = "green"
color_blue = "blue"

# GUI Initializing
root = Tk()  # create window
root.title(title)  # set window title
# width, height = root.winfo_screenwidth(), root.winfo_screenheight()  # get screen info for responsive GUI
# print(width, height)
width, height = 1024, 600
root.geometry("%dx%d+0+0" % (width, height))  # Set window size
root.resizable(FALSE, FALSE)  # set window can not resize
root.option_add("*font", "{} {} {}".format(font_name, font_size_label, font_style_bold))

# Menu Photo (call after create root only)
photo_pizza = PhotoImage(file="pizza.png")
photo_soup = PhotoImage(file="soup.png")
photo_spaghetti = PhotoImage(file="spaghetti.png")
photo_burger = PhotoImage(file="burger.png")
photo_frenchfried = PhotoImage(file="frenchfried.png")
photo_salmon = PhotoImage(file="salmon.png")
photo_hotdog = PhotoImage(file="hotdog.png")
photo_steak = PhotoImage(file="steak.png")
photo_salad = PhotoImage(file="salad.png")

ShopNameLabel = Label(root, text=restaurant_name, bg=color_pink, width=10)
ShopNameLabel.grid(row=0, columnspan=3, sticky=NSEW)

Menu1 = Button(root, text="Pizza", image=photo_pizza, compound=TOP, command=lambda: add_menu("Pizza"))
Menu1.grid(row=1, column=0, rowspan=3, sticky=NSEW)
Menu1.config(width=170)
Menu2 = Button(root, text="Soup", image=photo_soup, compound=TOP, command=lambda: add_menu("Soup"))
Menu2.grid(row=1, column=1, rowspan=3, sticky=NSEW)
Menu3 = Button(root, text="Spaghetti", image=photo_spaghetti, compound=TOP, command=lambda: add_menu("Spaghetti"))
Menu3.config(width=170)
Menu3.grid(row=1, column=2, rowspan=3, sticky=NSEW)

Menu4 = Button(root, text="Burger", image=photo_burger, compound=TOP, command=lambda: add_menu("Burger"))
Menu4.grid(row=4, column=0, rowspan=3, sticky=NSEW)
Menu5 = Button(root, text="French Fired", image=photo_frenchfried, compound=TOP,
               command=lambda: add_menu("French Fired"))
Menu5.grid(row=4, column=1, rowspan=3, sticky=NSEW)
Menu6 = Button(root, text="Salmon", image=photo_salmon, compound=TOP, command=lambda: add_menu("Salmon"))
Menu6.grid(row=4, column=2, rowspan=3, sticky=NSEW)

Menu7 = Button(root, text="Hot Dog", image=photo_hotdog, compound=TOP, command=lambda: add_menu("Hot Dog"))
Menu7.grid(row=7, column=0, rowspan=3, sticky=NSEW)
Menu8 = Button(root, text="Steak", image=photo_steak, compound=TOP, command=lambda: add_menu("Steak"))
Menu8.grid(row=7, column=1, rowspan=3, sticky=NSEW)
Menu9 = Button(root, text="Salad", image=photo_salad, compound=TOP, command=lambda: add_menu("Salad"))
Menu9.grid(row=7, column=2, rowspan=3, sticky=NSEW)

MenuListHeader = Label(root, text="รายการอาหารที่สั่ง", fg=color_red, bg=color_yellow)
MenuListHeader.grid(row=0, column=3, sticky=NSEW)
MenuListLabel = Text(root, font=(font_name, font_size_button, font_style_bold), width=26,
                     height=int(5 % height))
MenuListLabel.insert(0.0, "กรุณาเลือกเมนูอาหารทางด้านซ้ายมือ")
MenuListLabel.configure(state=DISABLED)
MenuListLabel.grid(row=1, column=3, rowspan=8, sticky=NSEW)

CancelButton = Button(root, text="ล้างรายการ", fg=color_red, command=lambda: cancel_menu())
CancelButton.grid(row=8, column=3, sticky=NSEW)
CheckBillButton = Button(root, text="ทำรายการ", fg=color_green, command=lambda: start_cal())
CheckBillButton.grid(row=9, column=3, sticky=NSEW)

root.mainloop()
