
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

values=['인문과학', '사회과학', '공학', '자연과학',
        '교육학', '의약학', '예술ㆍ체육']

class App:
    def __init__(self):
        self.tk = Tk()
        self.tk.title('E-Class')
        self.tk.geometry('1080x720')
        self.tk.resizable(False, False)


        self.items = []
        self.books = []
        self.bookmarkname=''
        self.homepage_url = ''
        self.email_address=''
        
        self.dateStart = ''
        self.dateEnd = ''

        self.initData()

        self.initBanner()
        self.initSearchingArea()
        self.initClassListArea()
        self.initBookmarkListArea()
        self.initBody()

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

    def updateBody(self, item):
        self.bodyImage = PhotoImage(file="no_image_icon.png")
        self.updateCanvas()

        self.bodyImageLabel.configure(width=250, height=250, image=self.bodyImage)
        self.bodyEntryTest['text'] = ''
        self.body_image=None
        for key, value in item.items():
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

    def updateCanvas(self):
        self.bookmarkCanvas.delete('value')
        count = dict()
        for d in values:
            count[d] = 0
        for d in self.books:
            taxon = d['taxon'].split('>')[0]
            count[taxon] += 1
        maxCount = int(max(count.values()))
        barW = (425 - 20) / 7
        height = 175
        if maxCount == 0:
            return
        for i, d in enumerate(values):
            x1 = 10+i*barW
            y1 = height-15-(height-30)*count[d]/maxCount
            x2 = 10+(i+1)*barW
            y2 = height-15
            self.bookmarkCanvas.create_rectangle(x1, y1, x2, y2, fill='light cyan', tags='value')
            self.bookmarkCanvas.create_text(10+(i+0.5)*barW, height-7, text=d, tags='value', anchor ='center')

    def selectClass(self, event):
        if event.widget.curselection():
            self.updateBody(self.items[event.widget.curselection()[0]])

    def selectClassInBookmarkList(self, event):
        if event.widget.curselection():
            self.updateBody(self.books[event.widget.curselection()[0]])

    def initData(self):
        pass

    def initBanner(self):
        self.banner = Frame(self.tk,bg='azure')
        self.banner.place(x=0, y=0, width=1080, height=100)
        self.logo=PhotoImage(file="e-class_logo.png")
        self.logo_label=Label(self.tk, bg='azure', image=self.logo)
        self.logo_label.place(x=0,y=0)

    def initSearchingArea(self):
        self.searchingArea = Frame(self.tk, bg= 'light cyan')
        self.searchingArea.place(x=0, y=100, width=450, height=60)
        #구분선이 왜 안생기지 정말 모르겠다

        self.searchComboBox1 = ttk.Combobox(self.searchingArea, width=8, values=values)
        self.searchComboBox1.place(x=5,y=5)
        self.searchComboBox2 = ttk.Combobox(self.searchingArea, width=8)
        self.searchComboBox2.place(x=85, y=5)
        self.searchComboBox3 = ttk.Combobox(self.searchingArea, width=8)
        self.searchComboBox3.place(x=165, y=5)

        self.searchDateGuide = Label(self.searchingArea, text='기간')
        self.searchDateGuide.place(x=265, y=5)
        self.searchDateStart = Entry(self.searchingArea, width=8)
        self.searchDateStart.place(x=305, y=6)
        self.searchDateEnd = Entry(self.searchingArea, width=8)
        self.searchDateEnd.place(x=385, y=6)

        self.searchButton = Button(self.searchingArea, text="검색", width=6, command=self.searchClass)
        self.searchButton.place(x=395, y=30)

        #검색 버튼
        self.searchComboBox1.set('주제 분류')

        self.searchDateStart.insert(INSERT, '20190101')
        self.searchDateEnd.insert(INSERT, '20191231')

    def initClassListArea(self):
        self.classListArea = Frame(self.tk,  bg='light cyan')
        self.classListArea.place(x=0, y=160, width=450, height=300)

        #self.classListText=Label(self.classListArea, text='강의 목록',relief="ridge",
                                 #background="",borderwidth=5, font=ft)
        self.classListImage= PhotoImage(file="class.png")
        self.classListImage_label = Label(self.classListArea,  bg='light cyan', image=self.classListImage)
        self.classListImage_label.place(x=0, y=0)

        self.bookmarkButton = Button(self.classListArea, width=14, text="북마크 등록/해제", command=self.clickBookmark)
        self.bookmarkButton.place(x=340, y=20)

        self.classListAreaFrame = Frame(self.classListArea,bg='white')
        self.classListAreaFrame.place(x=5, y=50)

        self.classListBoxScrollbar=Scrollbar(self.classListAreaFrame)
        self.classListBoxScrollbar.pack(side=RIGHT,fill=Y)

        self.classListBox=Listbox(self.classListAreaFrame, width=60, height=15, bg='azure', borderwidth=0,relief='ridge',
                           yscrollcommand=self.classListBoxScrollbar.set, selectmode=SINGLE)
        self.classListBox.pack()
        self.classListBox.bind('<<ListboxSelect>>', self.selectClass)

    def initBookmarkListArea(self):
        self.bookmarkListArea = Frame(self.tk,bg='light cyan')
        self.bookmarkListArea.place(x=0, y=460, width=450, height=260)

        ft=font.Font(family="맑은 고딕", size=12)
        #self.bookmarkListText=Label(self.bookmarkListArea, text='북마크 목록 (통계)', font=ft)
        self.bookmarkListImage = PhotoImage(file="bookmark.png")
        self.bookmarkListImage_label = Label(self.bookmarkListArea, bg='light cyan', image=self.bookmarkListImage)
        self.bookmarkListImage_label.place(x=5, y=0)

        self.bookmarkNotebook=ttk.Notebook(self.bookmarkListArea, width=435, height=180)
        self.bookmarkNotebook.place(x=5, y=50),
        
        self.bookmarkListAreaFrame = Frame(bg='white')
        self.bookmarkNotebook.add(self.bookmarkListAreaFrame, text='북마크 목록')
        
        self.bookmarkListBoxScrollbar=Scrollbar(self.bookmarkListAreaFrame)
        self.bookmarkListBoxScrollbar.pack(side=RIGHT,fill=Y)

        self.bookmarkListBox=Listbox(self.bookmarkListAreaFrame, bg='azure', width=60, height=12, borderwidth=0,relief='ridge',
                                     yscrollcommand=self.bookmarkListBoxScrollbar.set, selectmode=SINGLE)
        self.bookmarkListBox.pack()
        self.bookmarkListBox.bind('<<ListboxSelect>>', self.selectClassInBookmarkList)


        self.bookmarkCanvasFrame = Frame(bg='white')
        self.bookmarkNotebook.add(self.bookmarkCanvasFrame, text='조회수 그래프')

        self.bookmarkCanvas = Canvas(self.bookmarkCanvasFrame, bg='azure', width=435, height=175)
        self.bookmarkCanvas.pack()

        self.bookmarkSendEmailButton = Button(self.bookmarkListArea, width=15, text="북마크 메일 전송 ", command=self.insertmail)
        self.bookmarkSendEmailButton.place(x=330, y=7)

    def clickBookmark(self):
        item = None

        if self.classListBox.curselection():
            item = self.items[self.classListBox.curselection()[0]]
        elif self.bookmarkListBox.curselection():
            item = self.books[self.bookmarkListBox.curselection()[0]]

        if not item:
            return

        if not item['course_title'] in [e['course_title'] for e in self.books]:
            self.bookmarkListBox.insert(self.books.__len__(), item['course_title'])
            self.books.append(item)
        else:
            index = 0
            for i, d in enumerate(self.books):
                if d['course_title'] == item['course_title']:
                    self.books.remove(item)
                    self.bookmarkListBox.delete(i, i)

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
        gmail.sendmail(self.email_address,gmail.MakeHtmlDoc(self))
        self.email_entrybox.delete(0, 'end')
        


    def initBody(self):
        self.body = Frame(self.tk, bg='light cyan')
        self.body.place(x=450, y=100, width=630, height=620)

        ft=font.Font(family="맑은 고딕", size=12)
        self.bodyTitleImage = PhotoImage(file="title1.png")
        self.bodyTitleImage_Label = Label(self.body, bg='light cyan', image=self.bodyTitleImage)
        self.bodyTitleImage_Label.place(x=5, y=5)


        self.bodyImage = PhotoImage(file="no_image_icon.png")
        self.bodyImageLabel=Label(self.body, width=250, height=250, image=self.bodyImage)
        self.bodyImageLabel.place(x=375, y=125)
        
        ft=font.Font(family="맑은 고딕", size=12)
        self.bodyCategory=Label(self.body, text='분류 : ', font=ft)
        self.bodyCategory.place(x=5, y=40)

        ft=font.Font(family="맑은 고딕", size=20)
        self.bodyClassName=Label(self.body, text='강의이름 : ', anchor='nw', width=41, font=ft)
        self.bodyClassName.place(x=5, y=70)

        ft=font.Font(family="맑은 고딕", size=12)
        self.bodyClassProvider=Label(self.body, text='제공기관 : ', anchor='nw', font=ft)
        self.bodyClassProvider.place(x=5, y=125)

        self.bodyClassTerm=Label(self.body, text='강의학기 : ', anchor='nw', font=ft)
        self.bodyClassTerm.place(x=5, y=155)

        self.bodyClassLecturer=Label(self.body, text='교수자명 : ', anchor='nw', font=ft)
        self.bodyClassLecturer.place(x=5, y=185)

        ft=font.Font(family="맑은 고딕", size=10)
        self.bodyDescription=Label(self.body, text='강의내용', justify='left', anchor='nw', width=88, wraplength=620, font=ft)
        self.bodyDescription.place(x=5, y=420)

        self.bodyEntryTest=Label(self.body, text='테스트', justify='left', font=ft)
        self.bodyEntryTest.place(x=20, y=410)

        button=Button(self.tk, width=15, text="홈페이지 링크 버튼",command=self.click_homepage)
        button.place(x=940,y=70)

        #홈페이지 링크 버튼

    def click_homepage(self):
        webbrowser.open_new(self.homepage_url)

    def run(self):
        self.tk.mainloop()

app = App()
app.run()
