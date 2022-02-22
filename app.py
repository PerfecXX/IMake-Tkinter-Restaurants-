# GUI Library
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

# Google Sheet Library
from oauth2client.service_account import ServiceAccountCredentials
import gspread


def set_option_member(selected):
    if selected != 0:
        MemberNumberEntry.configure(state=NORMAL)
    else:
        MemberNumberEntry.configure(state=DISABLED)


def set_option_discount(selected):
    if selected != 0:
        DiscountCodeEntry.configure(state=NORMAL)
    else:
        DiscountCodeEntry.configure(state=DISABLED)


def cal_total_price():
    global total_price
    for key, val in menu_entry_list.items():
        if key in default_price and menu_entry_list[key] != 0:
            total_price += default_price[key] * val
    print("total", total_price)


def total_price_reset():  # in case user press "ทำรายการ" and close the window without do anything
    global total_price
    total_price = 0
    window.destroy()


def start_cal():
    cal_total_price()
    global window, MemberNumberEntry, DiscountCodeEntry, Menulist
    window = Toplevel()
    window.title("{} - ทำรายการ".format(restaurant_name))
    window.resizable(FALSE, FALSE)
    window.geometry("%dx%d+0+0" % (width, height))
    window.grab_set()

    Top_MenuHeader = Label(window, text="รายการอาหารที่สั่ง", fg=color_red, bg=color_yellow, width=25)
    Top_MenuHeader.grid(row=0, column=0, sticky=NSEW)

    TOP_PriceCal = Label(window, text="บัตรสมาชิก/ส่วนลด", fg=color_gold, bg=color_red, width=25)
    TOP_PriceCal.grid(row=0, column=1, sticky=NSEW)

    LEFTFrame = Frame(window)
    LEFTFrame.grid(row=1, column=0, sticky=NW)
    RIGHTFrame = Frame(window)
    RIGHTFrame.grid(row=1, column=1, sticky=NW)
    RIGHTFrame2 = Frame(window)
    RIGHTFrame2.grid(row=1, column=1, sticky=S, pady=165)

    Menulist = Text(LEFTFrame, width=30, height=9)
    Menulist.grid(row=1, column=0)
    copy_menu()
    Menulist.configure(state=DISABLED)

    MemberLabel = Label(RIGHTFrame, text="บัตรสมาชิก")
    MemberLabel.grid(row=0, column=0, sticky=W)
    MemberStringVar = StringVar()
    MemberDropDown = ttk.Combobox(RIGHTFrame, textvariable=MemberStringVar)
    MemberDropDown["values"] = ("ไม่มีหมายเลขบัตรสมาชิก", "มีหมายเลขบัตรสมาชิก")
    MemberDropDown["state"] = "readonly"
    MemberDropDown.bind("<<ComboboxSelected>>", lambda _: set_option_member(MemberDropDown.current()))
    MemberDropDown.current(0)
    MemberDropDown.grid(row=0, column=1, sticky=N)
    MemberNumberLabel = Label(RIGHTFrame, text="หมายเลขบัตรสมาชิก")
    MemberNumberLabel.grid(row=1, column=0)
    MemberNumberEntry = Entry(RIGHTFrame, width=21)
    MemberNumberEntry.configure(state=DISABLED)
    MemberNumberEntry.grid(row=1, column=1)

    DiscountLabel = Label(RIGHTFrame, text="บัตรส่วนลด")
    DiscountLabel.grid(row=2, column=0, sticky=W)
    DiscountStringVar = StringVar()
    DiscountDropDown = ttk.Combobox(RIGHTFrame, textvariable=DiscountStringVar)
    DiscountDropDown["values"] = ("ไม่มีบัตรส่วนลด", "ส่วนลด5%", "ส่วนลด10%", "ส่วนลด15%", "ส่วนลด20%")
    DiscountDropDown["state"] = "readonly"
    DiscountDropDown.bind("<<ComboboxSelected>>", lambda _: set_option_discount(DiscountDropDown.current()))
    DiscountDropDown.current(0)
    DiscountDropDown.grid(row=2, column=1, sticky=W)

    DiscountCodeLabel = Label(RIGHTFrame, text="รหัสบัตรส่วนลด")
    DiscountCodeLabel.grid(row=3, column=0, sticky=W)
    DiscountCodeEntry = Entry(RIGHTFrame, width=21)
    DiscountCodeEntry.configure(state=DISABLED)
    DiscountCodeEntry.grid(row=3, column=1, sticky=W)

    PaymentHeader = Label(RIGHTFrame2, text="ช่องทางการชำระเงิน", fg=color_yellow, bg=color_blue, width=31)
    PaymentHeader.grid(row=0, column=0, sticky=W)
    PaymentRadioVar = IntVar()
    Payment_Cash_Radio = Radiobutton(RIGHTFrame2, text="เงินสด", variable=PaymentRadioVar, value=1)
    Payment_Cash_Radio.grid(row=1, column=0, sticky=W)
    Payment_Cash_Radio = Radiobutton(RIGHTFrame2, text="บัตรเครดิต", variable=PaymentRadioVar, value=2)
    Payment_Cash_Radio.grid(row=1, column=0, sticky=W, padx=100)
    Payment_Cash_Radio = Radiobutton(RIGHTFrame2, text="จ่ายออนไลน์", variable=PaymentRadioVar, value=2)
    Payment_Cash_Radio.grid(row=1, column=0, sticky=W, padx=250)

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
