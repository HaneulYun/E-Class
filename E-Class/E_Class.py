
from tkinter import *
from tkinter import ttk
#from tkinter import ttk, font
#import tkinter.messagebox
import urllib
import http.client

import xml.etree.ElementTree as ET


conn = http.client.HTTPConnection("kocw.net")
conn.request("GET",
             "/home/api/handler.do?key=537adad829de4e65782196737ced103f35930363b8e30956&from=20170101&to=20170201&end_num=10"
             #"/home/api/handler.do?key=537adad829de4e65782196737ced103f35930363b8e30956&from=20100101&to=20200201&end_num=30000"
             )

req = conn.getresponse()

raw = req.read().decode('utf-8')

root = ET.fromstring(raw)

items = []
for item in root.find('list'):
    data = dict()
    for d in item:
        data[d.tag] = d.text
    items.append(data)


class App:
    def __init__(self):
        self.tk = Tk()
        self.tk.title('E-Class')
        self.tk.geometry('1080x720')
        self.tk.resizable(False, False)

        self.initData()

        self.initBanner()
        self.initSearchingArea()
        self.initClassListArea()
        self.initBookmarkListArea()
        self.initBody()

    def selectClass(self, event):
        self.bodyBox.delete('1.0', END)
        for key, value in items[event.widget.curselection()[0]].items():
            self.bodyBox.insert(INSERT, key)
            self.bodyBox.insert(INSERT, '\n\t\t')
            self.bodyBox.insert(INSERT, value)
            self.bodyBox.insert(INSERT, '\n\n')

    def initData(self):
        pass

    def initBanner(self):
        self.banner = Frame(self.tk)
        self.banner.place(x=0, y=0, width=1080, height=100)
        self.logo=PhotoImage(file="e-class_logo.png")
        self.logo_label=Label(self.tk,image=self.logo)
        self.logo_label.place(x=0,y=0)

    def initSearchingArea(self):
        self.searchingArea = Frame(self.tk, bg='green')
        self.searchingArea.place(x=0, y=100, width=450, height=50)

        SearchListBox1 = StringVar()
        SearchListBox1 = ttk.Combobox(textvariable=SearchListBox1, width=6)
        SearchListBox1.place(x=10,y=115)
        SearchListBox2 = StringVar()
        SearchListBox2 = ttk.Combobox(textvariable=SearchListBox1, width=6)
        SearchListBox2.place(x=80, y=115)
        SearchListBox3 = StringVar()
        SearchListBox3 = ttk.Combobox(textvariable=SearchListBox1, width=6)
        SearchListBox3.place(x=150, y=115)
        #combobox 3개

        InputLabel = Entry(self.tk, width=25, borderwidth=2, relief='ridge')
        InputLabel.pack()
        InputLabel.place(x=220, y=115)
        #검색하는 박스

        SearchButton = Button(self.tk, text="검색") #command 추가해야함
        SearchButton.pack()
        SearchButton.place(x=410, y=113)
        #검색 버튼

    def initClassListArea(self):
        self.classListArea = Frame(self.tk, bg='blue')
        self.classListArea.place(x=0, y=150, width=450, height=350)

        ClassListBoxScrollbar=Scrollbar(self.classListArea)
        ClassListBoxScrollbar.pack(side=RIGHT,fill=Y)

        self.classListBox=Listbox(self.classListArea, width=60, height=40, borderwidth=2,relief='ridge',
                           yscrollcommand=ClassListBoxScrollbar.set, selectmode=SINGLE)
        #리스트박스일 경우
        self.classListBox.pack()

        for i, d in enumerate(items):
             self.classListBox.insert(i, d['course_id'])
        
        self.classListBox.bind('<<ListboxSelect>>', self.selectClass)

    def initBookmarkListArea(self):
        self.bookmarkListArea = Frame(self.tk, bg='yellow')
        self.bookmarkListArea.place(x=0, y=500, width=450, height=220)

    def initBody(self):
        self.body = Frame(self.tk, bg='white')
        self.body.place(x=450, y=100, width=630, height=620)

        BodyBoxScrollbar = Scrollbar(self.body)
        BodyBoxScrollbar.pack(side=RIGHT, fill=Y)
        self.bodyBox = Text(self.body, width=80, height=50, borderwidth=2, relief='ridge',
                            yscrollcommand=BodyBoxScrollbar.set)
        self.bodyBox.pack()
        self.bodyBox.place(x=30,y=0)

    def run(self):
        self.tk.mainloop()

app = App()
app.run()
