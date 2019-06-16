
from tkinter import *
from tkinter import ttk, font
import webbrowser
import gmail
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
        self.bookmarks = []
        self.bookmarkname=''
        self.homepage_url = ''
        self.email_address=''
        
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
            if 'course_title' in data.keys():
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
        #self.body4box.delete('1.0', END)
        #
        #self.body3box1.delete('1.0', END)
        #self.body3box2.delete('1.0', END)
        #self.body3box3.delete('1.0', END)
        #self.body3box4.delete('1.0', END)
        #self.body3box5.delete('1.0', END)
        self.bodyEntryTest['text'] = ''
        self.body_image=None
        for key, value in self.items[event.widget.curselection()[0]].items():
            if key == 'taxon':
                self.bodyCategory['text']='분류 : ' + value
            elif key == 'course_title':
                self.bodyClassName['text']='강의이름 : ' + value
                self.bookmarkname=value
            elif key == 'provider':
                self.bodyClassProvider['text']='제공기관 : ' + value
            elif key == 'term':
                self.bodyClassTerm['text']='강의학기 : ' + value
            elif key == 'lecturer':
                self.bodyClassLecturer['text']='교수자명 : ' + value
            elif key == 'thumbnail_url':
                with urllib.request.urlopen(value) as u:
                    raw_data=u.read()
                im=Image.open(BytesIO(raw_data))
                self.bodyImage=ImageTk.PhotoImage(im)
                self.bodyImageLabel.configure(width=250, height=250, image=self.bodyImage)
            elif key == 'course_description':
                self.bodyDescription['text']='강의내용\n' + value

            elif key in ['list_num', 'course_id']:
                pass

            #elif key=='course_url':
            #    self.homepage_url=value
            else:
                string = '{:<10} : {}\n'.format(key, value)
                self.bodyEntryTest['text'] = self.bodyEntryTest['text'] + string

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
        self.bookmarkListBox.bind('<<ListboxSelect>>', self.selectClass)

    def click_bookmark(self):
        for i, d in enumerate(self.items):
            if 'course_title' in d.keys():
                if d['course_title']== self.bookmarkname:
                    self.bookmarkListBox.insert(i, d['course_title'])

    def clickout_bookmark(self):
        for i, d in enumerate(self.items):
            if 'course_title' in d.keys():
                if d['course_title'] == self.bookmarkname:
                    self.bookmarkListBox.delete(i, d['course_title'])
                    break


    #중복 처리해야함
    #북마크를 클릭했을 때 정보가 떠야함

    def insertmail(self):
        self.window = Tk()
        self.window.title('E-Class')
        self.window.geometry('200x200')
        self.email_Label = Label(self.window, text="받으실 메일 주소를 입력하세요")
        self.email_Label.place(x=10, y=10)
        self.email_entrybox = Entry(self.window, width=25)
        self.email_entrybox.place(x=10, y=35)
        self.email_OK = Button(self.window, text='확인', command=self.sendmail_bookmark)
        self.email_OK.place(x=80, y=60)

    def sendmail_bookmark(self):
        self.email_address = self.email_entrybox.get()
        self.email_entrybox.delete(0, 'end')
        


    def initBody(self):
        self.body = Frame(self.tk, bg='red')
        self.body.place(x=450, y=100, width=630, height=620)

        self.bodyImage = PhotoImage(file="e-class_logo.png")
        self.bodyImageLabel=Label(self.body, width=250, height=250, image=self.bodyImage)
        self.bodyImageLabel.place(x=375, y=90)
        
        ft=font.Font(family="맑은 고딕", size=12)
        self.bodyCategory=Label(self.body, text='분류 : ', font=ft)
        self.bodyCategory.place(x=5, y=5)

        ft=font.Font(family="맑은 고딕", size=20)
        self.bodyClassName=Label(self.body, text='강의이름 : ', anchor='nw', width=41, font=ft)
        self.bodyClassName.place(x=5, y=35)

        ft=font.Font(family="맑은 고딕", size=12)
        self.bodyClassProvider=Label(self.body, text='제공기관 : ', anchor='nw', font=ft)
        self.bodyClassProvider.place(x=5, y=90)

        self.bodyClassTerm=Label(self.body, text='강의학기 : ', anchor='nw', font=ft)
        self.bodyClassTerm.place(x=5, y=120)

        self.bodyClassLecturer=Label(self.body, text='교수자명 : ', anchor='nw', font=ft)
        self.bodyClassLecturer.place(x=5, y=150)

        ft=font.Font(family="맑은 고딕", size=10)
        self.bodyDescription=Label(self.body, text='강의내용', justify='left', anchor='nw', width=88, wraplength=620, font=ft)
        self.bodyDescription.place(x=5, y=420)

        self.bodyEntryTest=Label(self.body, text='테스트', justify='left', font=ft)
        self.bodyEntryTest.place(x=20, y=410)

        button = Button(self.tk, width=15, text="북마크 메일 전송 ", command=self.insertmail)
        button.place(x=670, y=70)

        button = Button(self.tk, width=5, text="북마크 ", command=self.click_bookmark)
        button.place(x=800, y=70)

        button = Button(self.tk, width=10, text="북마크 해제", command=self.clickout_bookmark)
        button.place(x=850, y=70)

        button=Button(self.tk, width=15, text="홈페이지 링크 버튼",command=self.click_homepage)
        button.place(x=940,y=70)

        #홈페이지 링크 버튼

    def click_homepage(self):
        webbrowser.open_new(self.homepage_url)

    def run(self):
        self.tk.mainloop()

app = App()
app.run()
