
from tkinter import *
from tkinter import ttk, font
import webbrowser
#from tkinter import ttk, font
#import tkinter.messagebox

from io import BytesIO
from PIL import Image, ImageTk

import urllib
import urllib.request
import http.client

import xml.etree.ElementTree as ET

class App:
    def __init__(self):
        self.tk = Tk()
        self.tk.title('E-Class')
        self.tk.geometry('1080x720')
        self.tk.resizable(False, False)

        self.items = []
        self.homepage_url = ''
        
        # self.category1 = ''
        # self.category2 = ''
        # self.category3 = ''
        self.dateStart = ''
        self.dateEnd = ''

        self.initData()

        self.initBanner()
        self.initSearchingArea()
        self.initClassListArea()
        self.initBookmarkListArea()
        self.initBody()

        # ####내가 한 곳###
        # self.v=IntVar()
        # radio1=Radiobutton(self.tk,text="리스트",variable=self.v,value=1, command=self.initClassListArea)
        # radio1.pack()
        # radio1.place(x=10,y=170)
        # 
        # radio2 = Radiobutton(self.tk, text="썸네일", variable=self.v, value=2) #command 썸네일일 때 되게 해야함
        # radio2.pack()
        # radio2.place(x=80, y=170)
        # ###내가 한 곳###

    def searchClass(self):
        id = self.searchComboBox1.current()
        self.dateStart = self.searchDateStart.get()
        self.dateEnd = self.searchDateEnd.get()

        if id < 0:
            return

        conn = http.client.HTTPConnection("kocw.net")
        conn.request("GET",
             "/home/api/handler.do?key=537adad829de4e65782196737ced103f35930363b8e30956&category_type=t&category_id=" + str(id+1) + "&from=" + str(self.dateStart) + "&to=" + str(self.dateEnd) + "&end_num=30000"
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
        self.body4box.delete('1.0', END)
        self.body3box1.delete('1.0', END)
        self.body3box2.delete('1.0', END)
        self.body3box3.delete('1.0', END)
        self.body3box4.delete('1.0', END)
        self.body3box5.delete('1.0', END)
        self.body_image=None
        for key, value in self.items[event.widget.curselection()[0]].items():
            if key == 'taxon':
                self.bodyCategory['text']='분류 : ' + value
                #self.body3box1.insert(INSERT, value)
            elif key == 'course_title':
                self.body3box2.insert(INSERT, value)
            elif key == 'lecturer':
                self.body3box3.insert(INSERT, value)
            elif key=='provider':
                self.body3box4.insert(INSERT, value)
            elif key=='term':
                self.body3box5.insert(INSERT, value)
            elif key=='thumbnail_url':
                with urllib.request.urlopen(value) as u:
                    raw_data=u.read()

                im=Image.open(BytesIO(raw_data))
                self.body_image=ImageTk.PhotoImage(im)
            elif key=='course_url':
                self.homepage_url=value
            else:
                string = '{:<20} : {}\n'.format(key, value)
                self.body4box.insert(INSERT, string)
        self.body_label.configure(image=self.body_image)

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
        self.searchingArea.place(x=0, y=100, width=450, height=60)

        values=['인문과학', '사회과학', '공학', '자연과학',
                '교육학', '의약학', '예술체육']

        self.searchComboBox1 = ttk.Combobox(self.searchingArea, width=8, values=values)
        self.searchComboBox1.place(x=5,y=5)
        self.searchComboBox2 = ttk.Combobox(self.searchingArea, width=8)
        self.searchComboBox2.place(x=85, y=5)
        self.searchComboBox3 = ttk.Combobox(self.searchingArea, width=8)
        self.searchComboBox3.place(x=165, y=5)

        self.searchDateGuide = Label(self.searchingArea, text='기간', bg='green')
        self.searchDateGuide.place(x=265, y=5)
        self.searchDateStart = Entry(self.searchingArea, width=8)
        self.searchDateStart.place(x=305, y=6)
        self.searchDateEnd = Entry(self.searchingArea, width=8)
        self.searchDateEnd.place(x=385, y=6)

        #combobox 3개
        # InputLabel = Entry(self.searchingArea, width=20, borderwidth=2, relief='ridge')
        # InputLabel.place(x=250, y=15)
        # #검색하는 박스

        self.searchButton = Button(self.searchingArea, text="검색", width=6, command=self.searchClass)
        self.searchButton.place(x=395, y=30)

        #검색 버튼
        self.searchComboBox1.set('주제 분류')

        self.searchDateStart.insert(INSERT, '20190101')
        self.searchDateEnd.insert(INSERT, '20191231')

    def initClassListArea(self):
        self.classListArea = Frame(self.tk, bg='blue')
        self.classListArea.place(x=0, y=160, width=450, height=360)

        self.classListAreaFrame = Frame(self.classListArea)
        self.classListAreaFrame.place(x=5, y=5)

        self.classListBoxScrollbar=Scrollbar(self.classListAreaFrame)
        self.classListBoxScrollbar.pack(side=RIGHT,fill=Y)

        self.classListBox=Listbox(self.classListAreaFrame, width=60, height=21, borderwidth=0,relief='ridge',
                           yscrollcommand=self.classListBoxScrollbar.set, selectmode=SINGLE)
        self.classListBox.pack()
        self.classListBox.bind('<<ListboxSelect>>', self.selectClass)

    def initBookmarkListArea(self):
        self.bookmarkListArea = Frame(self.tk, bg='yellow')
        self.bookmarkListArea.place(x=0, y=520, width=450, height=200)
        
        self.bookmarkListAreaFrame = Frame(self.bookmarkListArea)
        self.bookmarkListAreaFrame.place(x=5, y=5)
        
        self.bookmarkListBoxScrollbar=Scrollbar(self.bookmarkListAreaFrame)
        self.bookmarkListBoxScrollbar.pack(side=RIGHT,fill=Y)

        self.bookmarkListBox=Listbox(self.bookmarkListAreaFrame, width=60, height=11, borderwidth=0,relief='ridge',
                                     yscrollcommand=self.bookmarkListBoxScrollbar.set, selectmode=SINGLE)
        self.bookmarkListBox.pack()

    def initBody(self):
        self.body = Frame(self.tk, bg='red')
        self.body.place(x=450, y=100, width=630, height=620)

        self.body_image = None
        self.body_label=Label(self.body, image=self.body_image)
        #self.body_label.place(x=5, y=5)
        
        #이미지
        self.body2=Frame(self.tk,bg="orange")
        #self.body2.place(x=760, y=100, width=290,height=300)
        
        ft=font.Font(family="맑은 고딕", size=12)
        self.bodyCategory=Label(self.body, text='분류 : ', font=ft)
        self.bodyCategory.place(x=5, y=5)
        #self.body2box1.place(x=750,y=100)
        self.body2box2 = Label(self.tk, width=15, height=4, text="강의이름")
        #self.body2box2.place(x=750, y=160)
        self.body2box3 = Label(self.tk, width=15, height=4, text="교수자명")
        #self.body2box3.place(x=750, y=220)
        self.body2box4 = Label(self.tk, width=15, height=4, text="제공기관")
        #self.body2box4.place(x=750, y=280)
        self.body2box5 = Label(self.tk, width=15, height=4, text="강의학기")
        #self.body2box5.place(x=750, y=340)
        #주제분류, 강의이름, 강의자, 제공기관, 강의기간
        
        self.body3=Frame(self.tk)
        #self.body3.place(x=860, y=100, width=190, height=300)
        #그에 따른 실제 내용
        
        self.body3box1 = Text(self.tk, width=27, height=4,borderwidth=2)
        #self.body3box1.place(x=860, y=100)
        self.body3box2 = Text(self.tk, width=27, height=4, borderwidth=2)
        #self.body3box2.place(x=860, y=160)
        self.body3box3 = Text(self.tk, width=27, height=4, borderwidth=2)
        #self.body3box3.place(x=860, y=220)
        self.body3box4 = Text(self.tk, width=27, height=4, borderwidth=2)
        #self.body3box4.place(x=860, y=280)
        self.body3box5 = Text(self.tk, width=27, height=4, borderwidth=2)
        #self.body3box5.place(x=860, y=340)
        
        self.body4=Frame(self.tk, bg='pink')
        #self.body4.place(x=460, y=410, width=600, height=300)
        #강의소개, 홈페이지 링크
        
        BodyBoxScrollbar = Scrollbar(self.body4)
        #BodyBoxScrollbar.pack(side=RIGHT, fill=Y)
        self.body4box = Text(self.body4, width=80, height=50, borderwidth=2, relief='ridge',
                           yscrollcommand=BodyBoxScrollbar.set)
        #self.body4box.pack()
        #self.body4box.place(x=20,y=0)
        
        
        button=Button(self.tk, width=15, text="홈페이지 링크 버튼",command=self.click_homepage)
        button.place(x=940,y=70)
        #홈페이지 링크 버튼

    def click_homepage(self):
        webbrowser.open_new(self.homepage_url)

    def run(self):
        self.tk.mainloop()

app = App()
app.run()
