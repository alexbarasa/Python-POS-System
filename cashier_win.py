import errno
import random
import sqlite3
import tkinter as tk
import tkinter.simpledialog as sd
from datetime import datetime
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
from tkinter.ttk import Style
from PIL import Image, ImageTk
import os
from sys import exit
import time


class CashierWin():
    def __init__(self, master, ID=''):
        self.cashWin = master
        self.cashWin.resizable(0, 0)
        self.cashWin.protocol("WM_DELETE_WINDOW", exit)
        self.windowHeight = int(self.cashWin.winfo_reqheight())
        self.windowWidth = int(self.cashWin.winfo_reqwidth())
        self.positionRight = int(self.cashWin.winfo_screenwidth() / 2 - (self.windowWidth / 2))
        self.positionDown = int(self.cashWin.winfo_screenheight() / 2 - (self.windowHeight / 2))
        self.cashWin.iconphoto(False, PhotoImage(file='images/rozeriya.png'))
        self.cashWin.geometry(f"1400x800")
        self.cashWin.title("ADMIN FORM")
        style = Style()
        style.configure('W.TButton', font=('Comic sans ms', 15, 'normal', 'italic'), foreground='black')
        style1 = 'W.TButton'

        # Setup Var
        self.IDcashier = ID
        self.dateNow = datetime.now().strftime("%d/%b/%Y")
        self.n = 0
        self.k = 0
        self.p = 0
        self.dbPath = '//Zerozed-pc/shared/DB/ROZERIYA-DB.db'
        self.totalMoney = 0
        self.totalBuy = 0
        self.printIntro = True
        self.buy = []
        self.counting = True
        self.memberDeal = []
        self.calcChoice = True
        self.dealDiscount = 0
        self.memberDiscount = 0

        # Cashier Name
        def name():
            conn = sqlite3.connect(self.dbPath)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM EMPLOYEE_DATA ORDER BY EMPLOYEE_ID;")
            query1 = cursor.fetchall()
            name = []
            for i in query1:
                for x in i:
                    name.append(str(x))

            cashierName = 'NAME: ' + str(name[name.index(self.IDcashier) + 1])
            nameLen = len(list(map(len, cashierName)))
            wordLen = list(map(len, cashierName.split(" ")))

            namelbl = Label(self.cashWin, text=cashierName, font=('comic sans ms', 13, 'bold'),
                            foreground='blue')
            namelbl.place(relx=0, rely=0.041)

        # product detail
        def productDetail(*args):
            conn = sqlite3.connect(self.dbPath)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PRODUCT_DATA ORDER BY PRODUCT_ID;")
            query1 = cursor.fetchall()
            product = []
            for i in query1:
                for x in i:
                    product.append(str(x))

            try:
                self.Qty_entry.config(state='normal')
                self.Price_entry.config(state='normal')
                self.ID_entry.config(state='disabled')
                self.cancelButton.config(state='normal')
                self.Qty_entry.focus_set()
                self.productName = str(product[product.index(self.getPrdID.get()) + 1])
                self.namePrd = Label(self.cashWin, text="Product Name: " + self.productName + "                       ",
                                     font=('comic sans ms', 15, 'bold'))
                self.namePrd.place(relx=0, rely=0.4)
                productQty = int(product[product.index(self.getPrdID.get()) + 4])
                self.qtyPrd = Label(self.cashWin,
                                    text="KUANTITI: " + str(productQty) + "     ",
                                    font=('comic sans ms', 15, 'bold'))
                if productQty <= 20:
                    self.qtyPrd.config(foreground='red')
                    messagebox.showwarning("Stok", "ISI STOK DENGAN SEGERA")
                elif productQty <= 0:

                    self.qtyPrd.config(foreground='red')
                    messagebox.showwarning("Stok", "ITEM SUDAH KEHABISAN STOK")
                self.qtyPrd.place(relx=0, rely=0.45)
                productPrice = float(product[product.index(self.getPrdID.get()) + 3])
                self.getPrdPrice.set(productPrice)

            except:
                self.getPrdID.set('')
                self.Qty_entry.config(state='disabled')
                self.Price_entry.config(state='disabled')
                self.ID_entry.config(state='normal')
                self.cancelButton.config(state='disabled')
                messagebox.showerror("ERROR", "PRODUCT ID NOT FOUND OR ENTRY EMPTY")

        # background
        background_image = tk.PhotoImage(master=self.cashWin, file='images/cashierbg.png')
        background_label = Label(self.cashWin, background='gold', image=background_image)
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # ID
        self.idCashlbl = Label(self.cashWin, text='ID: ' + self.IDcashier, font=('comic sans ms', 15, 'bold'),
                               foreground='green')
        self.idCashlbl.place(relx=0, rely=0, width=238)
        name()

        # TIME
        self.timeString = StringVar()
        Label(self.cashWin, text='TIME: ', font=('comic sans ms', 12, 'bold'),
              foreground='black').place(relx=0.6, rely=0.041)
        self.timelbl = Label(self.cashWin, text='', textvariable=self.timeString, font=('comic sans ms', 12, 'bold'),
                             foreground='green')
        self.timelbl.place(relx=0.64, rely=0.041, width=238)
        self.timelbl.after(1, self.updateTime)

        # DATE
        Label(self.cashWin, text='DATE: ' + datetime.now().strftime("%d/%b/%Y"), font=('comic sans ms', 13, 'bold'),
              foreground='black').place(relx=0.6, rely=0.005)

        # back button
        self.backButton = Button(self.cashWin, text='BACK', style=style1, command=self.backChoice)
        self.backButton.place(relx=0.9, rely=0)

        # total button
        self.totalButton = Button(self.cashWin, text='TOTAL', style=style1, command=self.payWindow)
        self.totalButton.place(relx=0.5, rely=0.95)

        # cancel sale button
        self.cancelSaleButton = Button(self.cashWin, text='SALE CANCEL', style=style1, command=self.saleCancel)
        self.cancelSaleButton.place(relx=0.5, rely=0.85)

        # Intro
        self.scrollbar = Scrollbar(self.cashWin)
        # self.scrollbar.place(relx=0.8, rely=0.5, height=400)
        self.outputArea = Text(self.cashWin)
        self.outputArea.config(state='disabled', yscrollcommand=self.scrollbar.set)
        self.outputArea.place(relx=0.6, rely=0.2, relwidth=0.4, relheight=0.15)

        # Treeview buy
        cols = ('ID', 'PRODUK', 'QTY', 'HARGA(RM)', 'TOTAL(RM)')
        self.buyScreen = Treeview(self.cashWin, columns=cols, show='headings')
        i = 0
        for col in cols:
            i = i + 1
            if i == 1:
                self.buyScreen.heading(col, text=col, )
                self.buyScreen.column(col, minwidth=0, width=140, stretch=False)
            elif i == 2:
                self.buyScreen.heading(col, text=col, )
                self.buyScreen.column(col, minwidth=0, width=225, stretch=False)
            elif i == 3:
                self.buyScreen.heading(col, text=col, )
                self.buyScreen.column(col, minwidth=0, width=45, stretch=False)
            elif i == 4:
                self.buyScreen.heading(col, text=col, )
                self.buyScreen.column(col, minwidth=0, width=75, stretch=False)
            elif i == 5:
                self.buyScreen.heading(col, text=col, )
                self.buyScreen.column(col, minwidth=0, width=75, stretch=False)

        # insert to buy

        self.buyScreen.place(relx=0.6, rely=0.35, relwidth=0.4, relheight=0.35)
        vsb = Scrollbar(self.cashWin, orient="vertical", command=self.buyScreen.yview)
        # vsb.place(relx=0.98, rely=0.1, relheight=0.5)
        hrz = Scrollbar(self.cashWin, orient="horizontal", command=self.buyScreen.xview)
        # hrz.place(relx=0.6, rely=0.7, relwidth=0.4)
        self.buyScreen.configure(yscrollcommand=vsb.set, xscrollcommand=hrz.set)

        # TOTAL PRICE
        self.scrollbarPrice = Scrollbar(self.cashWin)
        # self.scrollbar.place(relx=0.8, rely=0.5, height=400)
        self.totalPrice = Text(self.cashWin)
        self.totalPrice.config(state='disabled', yscrollcommand=self.scrollbarPrice.set)
        self.totalPrice.place(relx=0.6, rely=0.7, relwidth=0.4, relheight=0.35)

        # PRODUCT ID
        self.getPrdID = StringVar()
        Label(self.cashWin, text="ID", font=('arial', 15, 'bold')).place(relx=0, rely=0.28)
        self.ID_entry = Entry(self.cashWin, textvariable=self.getPrdID, font=('comic sans ms', 12, 'bold'))
        self.ID_entry.place(relx=0, rely=0.32, height=30, width=200)
        self.ID_entry.focus_set()

        # QUANTITY
        self.getPrdQty = IntVar()
        Label(self.cashWin, text="QTY", font=('arial', 15, 'bold')).place(relx=0.18, rely=0.28)
        self.Qty_entry = Entry(self.cashWin, textvariable=self.getPrdQty, font=('comic sans ms', 12, 'bold'),
                               state='disabled')
        self.Qty_entry.place(relx=0.18, rely=0.32, height=30, width=50)

        def q(*args):
            self.Qty_entry.selection_range(0, END)

        self.Qty_entry.bind("<FocusIn>", q)

        # PRICE
        self.getPrdPrice = DoubleVar()
        Label(self.cashWin, text="PRICE", font=('arial', 15, 'bold')).place(relx=0.25, rely=0.28)
        self.Price_entry = Entry(self.cashWin, textvariable=self.getPrdPrice, font=('comic sans ms', 12, 'bold'),
                                 state='disabled')
        self.Price_entry.place(relx=0.25, rely=0.32, height=30, width=100)

        def a(*args):
            self.Price_entry.selection_range(0, END)

        self.Price_entry.bind("<FocusIn>", a)

        self.ID_entry.bind("<Return>", productDetail)
        self.cashWin.bind("<Return>", self.insertBuy)

        # cancel button
        self.cancelButton = Button(self.cashWin, text='cancel', command=self.cancel, state='disabled')
        self.cancelButton.place(relx=0.35, rely=0.32)

        # buy count and total money
        Label(self.cashWin, text="TOTAL TODAY: RM" + str(self.totalMoney), font=('comic sans ms', 15, 'bold')).place(
            relx=0.6, rely=0.15)
        Label(self.cashWin, text="SALE NO: " + str(self.n), font=('comic sans ms', 15, 'bold')).place(relx=0.85,
                                                                                                      rely=0.15)

        # MEMBERCARD ENTRY AND DEAL ENTRY
        self.getMemberID = StringVar()
        Label(self.cashWin, text="MEMBERCARD ID", font=('arial', 15, 'bold')).place(relx=0, rely=0.78)
        self.member_entry = Entry(self.cashWin, textvariable=self.getMemberID, font=('comic sans ms', 12, 'bold'),
                                  state='normal')
        self.member_entry.place(relx=0, rely=0.82, height=30, width=180)

        # self.getDealID = StringVar()
        # Label(self.cashWin, text="DEAL OR DISCOUNT ID", font=('arial', 15, 'bold')).place(relx=0.2, rely=0.78)
        # self.deal_entry = Entry(self.cashWin, textvariable=self.getDealID, font=('comic sans ms', 12, 'bold'),
        #                         state='normal')
        # self.deal_entry.place(relx=0.2, rely=0.82, height=30, width=180)

        def c(*args):
            if self.getMemberID.get() != '' and len(self.memberDeal) != 1:
                self.memberDeal.append(self.getMemberID.get())
                self.member_entry.delete(0, END)
                messagebox.showinfo("SUCESS", "MEMBER ID ENTERED")
            else:
                messagebox.showwarning("EMPTY", "EMPTY ENTRY OR MEMBER ID EXIST")

        def d(*args):
            if self.getDealID.get() != '' and len(self.memberDeal) != 2:
                if len(self.memberDeal) == 0:
                    self.memberDeal.append(" ")
                self.memberDeal.append(self.getDealID.get())
                self.deal_entry.delete(0, END)
                messagebox.showinfo("SUCESS", "DEAL ID ENTERED")
            else:
                messagebox.showwarning("EMPTY", "EMPTY ENTRY")

        self.member_entry.bind("<Return>", c)
        # self.deal_entry.bind("<Return>", d)

        self.cashWin.mainloop()

    # resit
    def receiptIntro(self):
        filename = "//Zerozed-pc/shared/DB/temp/resit.txt"
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        if self.counting == True:
            self.n = self.n + 1
            self.p = self.p + 1
        self.outputArea.config(state='normal', yscrollcommand=self.scrollbar.set)
        conn = sqlite3.connect('//Zerozed-pc/shared/DB/ROZERIYA-DB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM EMPLOYEE_DATA ORDER BY EMPLOYEE_ID;")
        query1 = cursor.fetchall()
        name = []
        for i in query1:
            for x in i:
                name.append(str(x))

        cashierName = 'NAME: ' + str(name[name.index(self.IDcashier) + 1])
        nameLen = len(list(map(len, cashierName)))
        wordLen = list(map(len, cashierName.split(" ")))
        # print(wordLen)
        # print(self.n, self.p, self.k)
        self.sellID = 'RZ0000S00' + str(self.p)
        if self.n >= 10:
            self.sellID = 'RZ0000S0' + str(self.p)
        if self.n >= 100:
            self.sellID = 'RZ0000S' + str(self.p)
            if self.p == 1000:
                self.k = self.k + 1
                self.p = 0
        if self.n >= 1000:
            if self.p == 1000:
                self.k = self.k + 1
                self.p = 0
            self.sellID = 'RZ000' + str(self.k) + 'S' + str(self.p)
        if self.n >= 10000:
            if self.p == 1000:
                self.k = self.k + 1
                self.p = 0
            self.sellID = 'RZ00' + str(self.k) + 'S' + str(self.p)
        if self.n >= 100000:
            if self.p == 1000:
                self.k = self.k + 1
                self.p = 0
            self.sellID = 'RZ0' + str(self.k) + 'S' + str(self.p)
        if self.n >= 100000:
            if self.p == 1000:
                self.k = self.k + 1
                self.p = 0
            self.sellID = 'RZ' + str(self.k) + 'S' + str(self.p) + "\n"
        self.counting = True

        # print(self.n, '', self.sellID)

        def insertData():
            intro = """ROZERIYA ENTERPRISE\nLOT 1784 KG RAHMAT 18000\nKUALA KRAI, KELANTAN\nTERIMA KASIH KERANA MEMBELI DENGAN KAMI""" + \
                    "\n__________________________________________________________________" \
                    ""
            resitComp = """__________________________________\n
item\t          Qty    S/Price    Amount"""  # 2/slash

            self.outputArea.insert(1.0, intro, 'CENTER')
            date = f"DATE&TIME: {str(self.dateNow)} {str(time.strftime('%H:%M:%S%p'))} \n"
            self.outputArea.insert(INSERT, "")
            self.outputArea.insert(INSERT, f"\nID:{self.IDcashier}\n")
            self.outputArea.insert(INSERT, f"CASHIER:{str(name[name.index(self.IDcashier) + 1])}\n")
            self.outputArea.insert(INSERT, date)
            self.outputArea.insert(INSERT, f"SELL ID:{self.sellID}\n")
            self.outputArea.insert(INSERT, resitComp)
            self.outputArea.config(state='disabled', yscrollcommand=self.scrollbar.set)
            self.introGet = self.outputArea.get(1.0, END)
            with open(filename, "w") as f:
                f.write(self.introGet)
                f.close()

        # print(self.outputArea.get(1.0, END))
        insertData()
        # print(self.outputArea.get(1.0, END))

    # total SEND
    def payWindow(self):
        def paying():
            try:
                for i in self.buyScreen.get_children():
                    pass
                if i is not None:
                    self.totalCalc()
                    self.payWin = Toplevel(self.cashWin)
                    self.payWin.lift(aboveThis=self.cashWin)
                    self.payWin.resizable(0, 0)
                    self.payWin.protocol("WM_DELETE_WINDOW", False)
                    self.payWin.iconphoto(False, PhotoImage(file='images/rozeriya.png'))
                    self.payWin.geometry(f"800x500")
                    self.payWin.title("ADMIN FORM")
                    style = Style()
                    style.configure('Fun.TButton', font=('arial', 12, 'normal', 'italic'), foreground='black')
                    style1 = 'Fun.TButton'
                    # background
                    # background_image = tk.PhotoImage(master=self.payWin, file='images/cashierbg.png')
                    background_label = Label(self.payWin, background='silver')
                    # background_label.image = background_image
                    background_label.place(x=0, y=0, relwidth=1, relheight=1)

                    # main frame
                    payFrame = Frame(self.payWin)
                    payFrame.place(relheight=1, relwidth=0.8, relx=0.2)
                    payFrame_bg = Label(payFrame, background='dark blue')
                    payFrame_bg.place(x=0, y=0, relwidth=1, relheight=1)

                    def cash():
                        filename = "//Zerozed-pc/shared/DB/temp/resit.txt"
                        if not os.path.exists(os.path.dirname(filename)):
                            try:
                                os.makedirs(os.path.dirname(filename))
                            except OSError as exc:  # Guard against race condition
                                if exc.errno != errno.EEXIST:
                                    raise
                        Label(payFrame, text="TOTAL:RM" + str(self.actualTotal),
                              font=('comic sans ms', 18, 'bold')).place(relx=0.35, rely=0.15)
                        self.getCash = DoubleVar()
                        Label(payFrame, text="RM:", font=('arial', 20, 'bold')).place(relx=0.15, rely=0.35)
                        self.payCash_entry = Entry(payFrame, textvariable=self.getCash,
                                                   font=('comic sans ms', 20, 'bold'),
                                                   state='enabled')
                        self.payCash_entry.place(relx=0.25, rely=0.35, height=30, width=200)
                        self.payCash_entry.focus_set()

                        def a(*args):
                            if self.getCash.get() >= self.actualTotal:
                                calcChange = round(self.getCash.get(), 2) - self.actualTotal
                                self.totalPrice.config(state='normal', yscrollcommand=self.scrollbarPrice.set)
                                self.totalPrice.insert(INSERT, f"CASH \t=RM{self.getCash.get()}\n")
                                self.totalPrice.insert(INSERT, f"CHANGE\t=RM{round(calcChange, 2)}\n")
                                self.totalGet = self.totalPrice.get(1.0, END)
                                self.totalPrice.config(state='disabled', yscrollcommand=self.scrollbarPrice.set)
                                with open(filename, "a") as f:
                                    f.write(self.totalGet)
                                    f.close()
                                self.totalCmd()
                                self.payWin.destroy()
                                self.totalMoney = self.totalMoney + self.actualTotal
                                Label(self.cashWin, text="TOTAL TODAY: RM" + str(self.totalMoney),
                                      font=('comic sans ms', 15, 'bold')).place(
                                    relx=0.6, rely=0.15)
                            else:
                                messagebox.showwarning("less cash", "cash is not enough")
                                self.payWin.lift(aboveThis=self.cashWin)


                        self.payCash_entry.bind("<Return>", a)

                        def b(*args):
                            self.payCash_entry.selection_range(0, END)

                        self.payCash_entry.bind("<FocusIn>", b)

                    def back():
                        self.totalPrice.config(state='normal', yscrollcommand=self.scrollbarPrice.set)
                        self.totalPrice.delete(1.0, END)
                        self.totalPrice.config(state='disabled', yscrollcommand=self.scrollbarPrice.set)
                        self.payWin.destroy()

                    # CASH BUTTON
                    self.payCash_Button = Button(self.payWin, text='CASH', command=cash, state='enabled', style=style1)
                    self.payCash_Button.place(relx=0, rely=0.15, height=50, width=160)

                    # CARD BUTTON
                    self.payCard_Button = Button(self.payWin, text='''CREDIT/DEBIT\nCARD''', command=None,
                                                 state='disabled', style=style1)
                    self.payCard_Button.place(relx=0, rely=0.3, height=50, width=160)

                    # CHEQUE BUTTON
                    self.payCheque_Button = Button(self.payWin, text='CHEQUE', command=None, state='disabled',
                                                   style=style1)
                    self.payCheque_Button.place(relx=0, rely=0.45, height=50, width=160)

                    # CHEQUE BUTTON
                    self.payInstallment_Button = Button(self.payWin, text='INSTALLMENT', command=None, state='disabled',
                                                        style=style1)
                    self.payInstallment_Button.place(relx=0, rely=0.6, height=50, width=160)

                    # BACK BUTTOn
                    self.backPayWin_Button = Button(self.payWin, text='BACK', command=back, state='normal',
                                                    style=style1)
                    self.backPayWin_Button.place(relx=0, rely=0.75, height=50, width=160)
                else:
                    messagebox.showwarning("SALE INPUT", "NO SALE INPUT TO TOTAL")
            except:
                messagebox.showwarning("SALE INPUT", "NO SALE INPUT TO TOTAL")

        try:
            for i in self.buyScreen.get_children():
                pass
            if i is not None:
                if len(self.memberDeal) == 0 or len(self.memberDeal) == 1:
                    if len(self.memberDeal) == 0:
                        findMember = messagebox.askquestion("MEMBER ID", "MEMBER ID?", icon='info')
                        if findMember == 'yes':
                            findMemberID = sd.askstring(title="MEMBER ID ", prompt="INSERT MEMBER ID")
                            self.memberDeal.append(str(findMemberID))

                    # findDeal = messagebox.askquestion("DEAL ID", "DEAL ID?", icon='info')
                    # if findDeal == 'yes':
                    #     findDealID = sd.askstring(title="DEAL ID ", prompt="INSERT DEAL ID")
                    #     if len(self.memberDeal) == 0:
                    #         self.memberDeal.append("")
                    #     self.memberDeal.append(str(findDealID))
                    # for i in range(2):
                    #     if self.memberDeal != 2:
                    #         self.memberDeal.append("")

                print(self.memberDeal)
                def useDeals():
                    from data.callDB import callDB
                    db = callDB()
                    db.cursor.execute(f"SELECT * FROM DEAL")
                    db.conn.commit()
                    rawValue = db.cursor.fetchall()
                    c = 0
                    getV = []
                    for p in rawValue:
                        for i in p:
                            getV.append(i)
                            if len(getV) > c:
                                self.deals(id=getV[c])
                                print(getV[c])
                                c=c+3

                useDeals()
                paying()

            else:
                messagebox.showwarning("SALE INPUT", "NO SALE INPUT TO TOTAL Else")
        except Exception as e:
            print(e)
            messagebox.showwarning("SALE INPUT", "NO SALE INPUT TO TOTAL excpt")

    def totalCmd(self):
        def printResult():
            result = messagebox.askquestion("RECEIPT", "Print The Receipt?", icon='info')
            if result == 'yes':
                print("sent to the printer")
                self.outputArea.config(state='normal')
                self.outputArea.delete(1.0, END)
                self.outputArea.config(state='disabled', yscrollcommand=self.scrollbar.set)
                self.totalPrice.config(state='normal', yscrollcommand=self.scrollbarPrice.set)
                self.totalPrice.delete(1.0, END)
                self.totalPrice.config(state='disabled', yscrollcommand=self.scrollbarPrice.set)
                for i in self.buyScreen.get_children():
                    self.buyScreen.delete(i)
                os.startfile(r"\\Zerozed-pc\shared\DB\temp\resit.txt", 'print')
            else:
                print("not sent to the printer")
                self.outputArea.config(state='normal')
                self.outputArea.delete(1.0, END)
                self.outputArea.config(state='disabled', yscrollcommand=self.scrollbar.set)
                self.totalPrice.config(state='normal', yscrollcommand=self.scrollbarPrice.set)
                self.totalPrice.delete(1.0, END)
                for i in self.buyScreen.get_children():
                    self.buyScreen.delete(i)
                self.totalPrice.config(state='disabled', yscrollcommand=self.scrollbarPrice.set)

        self.ID_entry.focus_set()
        self.updateDb()
        self.printIntro = True
        self.counting = True
        Label(self.cashWin, text="SALE NO: " + str(self.n), font=('comic sans ms', 15, 'bold')).place(relx=0.85,
                                                                                                      rely=0.15)
        self.buy.clear()
        self.memberDeal.clear()
        self.outputArea.after(1000, printResult)

    # insert, cancel and calc config
    def insertBuy(self, *args):
        try:
            if self.printIntro is True:
                self.receiptIntro()
                self.printIntro = False
            if self.getPrdQty.get() != 0 and self.getPrdID != '':
                print("PRODUCT INSERT")
                self.ID_entry.focus_set()
                priceRound = round(float(self.getPrdPrice.get()), 2)
                self.calc = self.getPrdQty.get() * round(self.getPrdPrice.get(), 2)
                self.buyScreen.insert("", END,
                                      values=(
                                          self.getPrdID.get(), self.productName, str(self.getPrdQty.get()),
                                          str(priceRound),
                                          str(round(self.calc, 2))))
                self.buy.append(str(self.getPrdID.get()))
                self.buy.append(str(self.getPrdQty.get()))
                filename = "//Zerozed-pc/shared/DB/temp/resit.txt"
                if not os.path.exists(os.path.dirname(filename)):
                    try:
                        os.makedirs(os.path.dirname(filename))
                    except OSError as exc:  # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise
                with open(filename, "a") as f:
                    if len(self.productName) > 15:
                        shorter = self.productName[0]
                        for i in range(0, len(str(self.productName))):
                            if str(self.productName)[i] == " ":
                                shorter = shorter + str(self.productName)[i + 1]
                    else:
                        shorter = self.productName
                    productApd = f"""{self.productName}\n{self.getPrdID.get()}  {str(self.getPrdQty.get())}  RM{priceRound}  RM{round(self.calc, 2)}\n"""
                    f.write(productApd)
                    f.close()
                self.cancel()

            else:
                print("blank")

        except:
            messagebox.showerror("WRONG INPUT", "TRY AGAIN")

    def totalCalc(self, *args):
        filename = "//Zerozed-pc/shared/DB/temp/resit.txt"
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        component = []
        test = ''
        totalPrice = 0.00
        for child in self.buyScreen.get_children():
            component.append(self.buyScreen.item(child)["values"][4])
        for i in component:
            totalPrice = totalPrice + float(i)
        calcRounding = round(totalPrice - round(totalPrice, 1), 2)
        if calcRounding < 0:
            a = ''
        else:
            a = '-'
        self.totalPrice.config(state='normal', yscrollcommand=self.scrollbarPrice.set)
        self.totalPrice.insert(INSERT, f"\nSUBTOTAL: \tRM{totalPrice}\n")
        self.totalPrice.insert(INSERT, f"ROUNDING:\tRM{a}{calcRounding}\n")
        self.totalPrice.insert(INSERT, "========================================\n ")
        tax = open("data/tax.cfg")
        n = ''
        for i in tax.read():
            n = n + i
        self.actualTotal = totalPrice - calcRounding - self.dealDiscount
        self.totalPrice.insert(INSERT, f"\nTAX: {n} %\n")
        self.totalPrice.insert(INSERT, f"DISCOUNT =-RM{self.dealDiscount}\n")
        self.totalPrice.insert(INSERT, f"TOTAL\t=RM{round(self.actualTotal, 2)}\n")
        # self.totalPrice.insert(INSERT, f"MEMBER ID:{self.memberCard()}\n")
        self.totalPrice.config(state='disabled', yscrollcommand=self.scrollbarPrice.set)


        self.dealDiscount = 0

    def updateDb(self, *args):
        n = 0
        p = 1
        from data.callDB import callDB
        print(self.buy)
        for i in range(0, len(self.buy)):
            if len(self.buy) > n:
                db = callDB()
                db.cursor.execute(f"SELECT QUANTITY FROM PRODUCT_DATA WHERE PRODUCT_ID = '{self.buy[n]}'")
                db.conn.commit()
                rawValue = db.cursor.fetchone()
                for i in rawValue:
                    count = int(i) - int(self.buy[p])
                db.cursor.execute(f"UPDATE PRODUCT_DATA SET QUANTITY=? WHERE PRODUCT_ID = ?", (count, self.buy[n],))
                db.conn.commit()
                p = p + 2
                n = n + 2

    def saleCancel(self):
        self.ID_entry.focus_set()
        self.counting = False
        try:
            for i in self.buyScreen.get_children():
                self.buyScreen.delete(i)
            if i is not None:
                self.memberDeal.clear()
                self.outputArea.config(state='normal')
                self.outputArea.delete(1.0, END)
                self.outputArea.config(state='disabled', yscrollcommand=self.scrollbar.set)
                self.totalPrice.config(state='normal', yscrollcommand=self.scrollbarPrice.set)
                self.totalPrice.delete(1.0, END)
                self.totalPrice.config(state='disabled', yscrollcommand=self.scrollbarPrice.set)
                self.printIntro = True
            else:
                messagebox.showwarning("SALE INPUT", "NO SALE INPUT TO DELETE")
        except:
            messagebox.showwarning("SALE INPUT", "NO SALE INPUT TO DELETE")

    # data manipulate config
    def memberCard(self, *args, id=''):
        if id == '':
            pass
        else:
            try:
                try:
                    from data.callDB import callDB
                    db = callDB()
                    db.cursor.execute(f"SELECT * FROM MEMBER WHERE MEMBER_ID = '{id}'")
                    db.conn.commit()
                    rawValue = db.cursor.fetchone()
                    print(rawValue)

                    # 3 types of members Premium, Gold, Bronze
                    # premium discount -
                    # gold discount -
                    # bronze discount -

                    def Premium():
                        print("premium member")

                        rawItem = []
                        getType = []  # [0] id, [1] quantity,[2] price ,[3] total
                        n = 0
                        p = 0
                        for child in self.buyScreen.get_children():
                            for i in self.buyScreen.item(child)["values"]:
                                rawItem.append(i)
                        for a in range(0, len(rawItem)):
                            if len(rawItem) > n:
                                db.cursor.execute(f"SELECT * FROM PRODUCT WHERE PRODUCT_ID = '{rawItem[n]}'")
                                db.conn.commit()

                    try:
                        if rawValue[1] == "PREMIUM":
                            Premium()
                    except:
                        messagebox.showerror("MEMBER ID", "MEMBER ID NOT FOUND")


                except Exception as e:
                    messagebox.showerror("ERROR", f"MEMBER ID NOT FOUND")
            except Exception as e:
                messagebox.showerror("ERROR", f"ERROR: {e}")

    def deals(self, *args, id=''):
        if id == '':
            pass
        else:
            try:
                try:
                    print("DEALS with ID: ", id)
                    from data.callDB import callDB
                    db = callDB()
                    db.cursor.execute(f"SELECT * FROM DEAL_DATA WHERE DEAL_ID = '{id}'")
                    db.conn.commit()
                    rawValue = db.cursor.fetchone()
                    print(rawValue)

                    # BELI X DAPAT Y
                    def CODE1():

                        try:
                            if 'BELI' in str(rawValue[6]) and 'DAPAT' in str(rawValue[6]):
                                print("CODE 1")
                                rawItem = []
                                getType = []  # [0] id, [1] quantity,[2] price ,[3] total
                                n = 0
                                p = 0
                                for child in self.buyScreen.get_children():
                                    for i in self.buyScreen.item(child)["values"]:
                                        rawItem.append(i)
                                for a in range(0, len(rawItem)):
                                    if len(rawItem) > n:
                                        db.cursor.execute(f"SELECT * FROM PRODUCT WHERE PRODUCT_ID = '{rawItem[n]}'")
                                        db.conn.commit()
                                        # rawValue[1] = product_types, rawValue[2] = product_name
                                        if rawValue[2] != None:
                                            if db.cursor.fetchone()[1] == str(rawValue[2]):
                                                getType.append(rawItem[n])
                                                getType.append(rawItem[n + 2])

                                        elif rawValue[1] != None:
                                            if db.cursor.fetchone()[1] == str(rawValue[1]):
                                                print(db.cursor.fetchall())
                                                getType.append(rawItem[n])  # prd id
                                                getType.append(rawItem[n + 2])  # prd qty
                                                getType.append(rawItem[n + 3])  # prd price
                                                getType.append(rawItem[n + 4])  # prd total
                                        n = n + 5

                                print(getType)
                                n = 0
                                for i in range(0, len(getType)):
                                    if len(getType) > n:
                                        p = p + getType[n + 1]
                                        n = n + 4
                                x = int(rawValue[3])
                                y = float(rawValue[4])
                                toDiscount = (p - (p % x))
                                code1Discount = (toDiscount / x) * ((float(getType[2]) * x) - y)
                                print(code1Discount,'BELI ' + str(x) ,'DAPAT ' + str(y))
                                self.dealDiscount = self.dealDiscount + code1Discount
                            else:
                                print("find 1 else")
                        except:
                            print("find 1 except")

                    # LEBIH X 1 DAPAT Y
                    def CODE2():
                        try:
                            if 'LEBIH' in str(rawValue[6]) and 'DAPAT' in str(rawValue[6]):
                                print("CODE 2")
                                rawItem = []
                                getType = []  # [0] id, [1] quantity,[2] price ,[3] total
                                n = 0
                                p = 0
                                for child in self.buyScreen.get_children():
                                    for i in self.buyScreen.item(child)["values"]:
                                        rawItem.append(i)
                                for a in range(0, len(rawItem)):
                                    if len(rawItem) > n:
                                        db.cursor.execute(f"SELECT * FROM PRODUCT WHERE PRODUCT_ID = '{rawItem[n]}'")
                                        db.conn.commit()
                                        # rawValue[1] = product_types, rawValue[2] = product_name
                                        if rawValue[2] != None:
                                            if db.cursor.fetchone()[1] == str(rawValue[2]):
                                                getType.append(rawItem[n])
                                                getType.append(rawItem[n + 2])

                                        elif rawValue[1] != None:
                                            if db.cursor.fetchone()[1] == str(rawValue[1]):
                                                print(db.cursor.fetchall())
                                                getType.append(rawItem[n])  # prd id
                                                getType.append(rawItem[n + 2])  # prd qty
                                                getType.append(rawItem[n + 3])  # prd price
                                                getType.append(rawItem[n + 4])  # prd total
                                        n = n + 5

                                print(getType)
                                n = 0
                                for i in range(0, len(getType)):
                                    if len(getType) > n:
                                        p = p + getType[n + 1]
                                        n = n + 4
                                k = 0
                                x = int(rawValue[3])
                                y = float(rawValue[4])

                                if p >= x:
                                    k = k + (float(getType[2]) - y)
                                print(k)
                                toDiscount = k * int(getType[1])
                                code1Discount = toDiscount
                                print(code1Discount, 'LEBIH ' + str(x), '1 DAPAT ' + str(y))
                                self.dealDiscount = self.dealDiscount + code1Discount
                            else:
                                print("find 2 else")
                        except:
                            print(n, k, x, y)
                            print('find 2 except')

                    CODE1()
                    CODE2()


                except:
                    messagebox.showerror("ERROR", f"DEALS ID NOT FOUND")
            except:
                messagebox.showerror("ERROR", f"ERROR: {Exception}")

    # misc config
    def updateTime(self):
        self.timeGet = time.strftime('%H:%M:%S %p')
        self.timeString.set(self.timeGet)
        self.timelbl.after(1000, self.updateTime)

    def cancel(self, *args):
        self.Qty_entry.config(state='disabled')
        self.Price_entry.config(state='disabled')
        self.ID_entry.config(state='normal')
        self.ID_entry.focus_set()
        self.namePrd.destroy()
        self.qtyPrd.destroy()
        self.cancelButton.config(state='disabled')
        self.getPrdID.set('')
        self.getPrdPrice.set(0)
        self.getPrdQty.set(0)
        print("destroy")

    def backChoice(self):
        print("Back")
        from session_start import SessionStart
        self.cashWin.destroy()
        start_choice = SessionStart().auth(Tk())
        return start_choice

    # report GET


# CashierWin(Tk(), ID='RZ0000E005')
