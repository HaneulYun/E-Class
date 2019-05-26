
from tkinter import *
from tkinter import ttk, font

#from tkinter import ttk, font
#import tkinter.messagebox
import urllib
import http.client

import xml.etree.ElementTree as ET

class App:
    def __init__(self):
        self.tk = Tk()
        self.tk.title('E-Class')
        self.tk.geometry('1080x720')
        self.tk.resizable(False, False)

        self.items = []

        self.initData()

        self.initBanner()
        self.initSearchingArea()
        self.initClassListArea()
        self.initBookmarkListArea()
        self.initBody()

    def searchClass(self):
        id = self.searchComboBox1.current()

        if id < 0:
            return

        conn = http.client.HTTPConnection("kocw.net")
        conn.request("GET",
             "/home/api/handler.do?key=537adad829de4e65782196737ced103f35930363b8e30956&category_type=t&category_id=" + str(id+1) + "&from=20170101&to=20170201&end_num=999"
             #"/home/api/handler.do?key=537adad829de4e65782196737ced103f35930363b8e30956&category_type=t&category_id=1&from=20170101&to=20180201&end_num=10000"
             #"/home/api/handler.do?key=537adad829de4e65782196737ced103f35930363b8e30956&from=20100101&to=20200201&end_num=30000"
             )
        req = conn.getresponse()
        xml = req.read().decode('utf-8')

        root = ET.fromstring(xml)

        self.items.clear()
        for item in root.find('list'):
            data = dict()
            for d in item:
                data[d.tag] = d.text
            self.items.append(data)

        category = dict()

        for d in self.items:
            if 'taxon' in d.keys():
                taxon = d['taxon'].split('>')
        
                if not taxon[0] in category:
                    category[taxon[0]] = dict()
        
                if not taxon[1] in category[taxon[0]]:
                    category[taxon[0]][taxon[1]] = dict()
        
                if not taxon[2] in category[taxon[0]][taxon[1]]:
                    category[taxon[0]][taxon[1]][taxon[2]] = 0
        
        self.classListBox.delete(0, END)
        for i, d in enumerate(self.items):
            if 'course_title' in d.keys():
                self.classListBox.insert(i, d['course_title'])

    def selectClass(self, event):
        self.body4Box.delete('1.0', END)
        for key, value in self.items[event.widget.curselection()[0]].items():
            string = '{:<20} : {}\n'.format(key, value)
            self.body4Box.insert(INSERT, string)

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
        self.searchingArea.place(x=0, y=100, width=450, height=100)

        values=['인문과학', '사회과학', '공학', '자연과학',
                '교육학', '의약학', '예술체육']
        self.searchComboBox1 = ttk.Combobox(self.searchingArea, width=8, values=values)
        self.searchComboBox1.place(x=10,y=15)
        self.searchComboBox2 = ttk.Combobox(self.searchingArea, width=8)
        self.searchComboBox2.place(x=90, y=15)
        self.searchComboBox3 = ttk.Combobox(self.searchingArea, width=8)
        self.searchComboBox3.place(x=170, y=15)

        #combobox 3개

        InputLabel = Entry(self.searchingArea, width=20, borderwidth=2, relief='ridge')
        InputLabel.pack()
        InputLabel.place(x=250, y=15)
        #검색하는 박스

        SearchButton = Button(self.searchingArea, text="검색", command=self.searchClass)
        SearchButton.pack()
        SearchButton.place(x=410, y=13)
        #검색 버튼

        self.searchComboBox1.set('주제 분류')

    def initClassListArea(self):
        self.classListArea = Frame(self.tk, bg='blue')
        self.classListArea.place(x=0, y=200, width=450, height=350)

        ClassListBoxScrollbar=Scrollbar(self.classListArea)
        ClassListBoxScrollbar.pack(side=RIGHT,fill=Y)

        self.classListBox=Listbox(self.classListArea, width=60, height=20, borderwidth=2,relief='ridge',
                           yscrollcommand=ClassListBoxScrollbar.set, selectmode=SINGLE)
        #리스트박스일 경우
        self.classListBox.pack()

        self.classListBox.bind('<<ListboxSelect>>', self.selectClass)

    def initBookmarkListArea(self):
        self.bookmarkListArea = Frame(self.tk, bg='yellow')
        self.bookmarkListArea.place(x=0, y=500, width=450, height=220)

    def initBody(self):

        self.body = Frame(self.tk, bg='white')
        self.body.place(x=460, y=100, width=290, height=300)

        self.body_image=PhotoImage(file="")
        self.body_label=Label(self.tk, image=self.body_image)
        self.body_label.place(x=460, y=100)


        #이미지

        self.body2=Frame(self.tk,bg="green")
        self.body2.place(x=760, y=100, width=290,height=300)

        self.body2box1=Label(self.tk,  width=15, height=4, text="주제분류")
        self.body2box1.pack()
        self.body2box1.place(x=750,y=100)
        self.body2box2 = Label(self.tk, width=15, height=4, text="강의이름")
        self.body2box2.pack()
        self.body2box2.place(x=750, y=160)
        self.body2box3 = Label(self.tk, width=15, height=4, text="강의자")
        self.body2box3.pack()
        self.body2box3.place(x=750, y=220)
        self.body2box4 = Label(self.tk, width=15, height=4, text="제공기관")
        self.body2box4.pack()
        self.body2box4.place(x=750, y=280)
        self.body2box5 = Label(self.tk, width=15, height=4, text="강의기간")
        self.body2box5.pack()
        self.body2box5.place(x=750, y=340)
        #주제분류, 강의이름, 강의자, 제공기관, 강의기간

        self.body3=Frame(self.tk,bg="purple")
        self.body3.place(x=860, y=100, width=190, height=300)
        #그에 따른 실제 내용

        self.body3box1 = Text(self.tk, width=27, height=4,borderwidth=2)
        self.body3box1.pack()
        self.body3box1.place(x=860, y=100)
        self.body3box2 = Text(self.tk, width=27, height=4, borderwidth=2)
        self.body3box2.pack()
        self.body3box2.place(x=860, y=160)
        self.body3box3 = Text(self.tk, width=27, height=4, borderwidth=2)
        self.body3box3.pack()
        self.body3box3.place(x=860, y=220)
        self.body3box4 = Text(self.tk, width=27, height=4, borderwidth=2)
        self.body3box4.pack()
        self.body3box4.place(x=860, y=280)
        self.body3box5 = Text(self.tk, width=27, height=4, borderwidth=2)
        self.body3box5.pack()
        self.body3box5.place(x=860, y=340)

        self.body4=Frame(self.tk, bg='pink')
        self.body4.place(x=460, y=410, width=600, height=300)
        #강의소개, 홈페이지 링크

        BodyBoxScrollbar = Scrollbar(self.body4)
        BodyBoxScrollbar.pack(side=RIGHT, fill=Y)
        self.body4Box = Text(self.body4, width=80, height=50, borderwidth=2, relief='ridge',
                           yscrollcommand=BodyBoxScrollbar.set)
        self.body4Box.pack()
        self.body4Box.place(x=20,y=0)

    def run(self):
        self.tk.mainloop()

app = App()
app.run()
