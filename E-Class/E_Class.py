
from tkinter import *
from tkinter import ttk, font
import tkinter.messagebox
import urllib
import http.client

conn = http.client.HTTPConnection("kocw.net")
conn.request("GET",
             "home/api/handler.do?key=537adad829de4e65782196737ced103f35930363b8e30956&from=20170101&to=20170201")
# 임시로 해놓은 것
req = conn.getresponse()
print(req.status, req.reason)
print(req.read().decode('utf-8'))

g_Tk = Tk()
g_Tk.geometry("1080x720")  # 창 크기x, 창의 위치+
DataList = []


def InitTopText():
    TempFont = font.Font(g_Tk, size=50, weight='bold', family='Consolas')
    MainText = Label(g_Tk, font=TempFont, text="E-Class")
    MainText.pack()
    MainText.place(x=10)


def InitSearchListBox():
    SearchListBox = StringVar()
    SearchListBox = ttk.Combobox(textvariable=SearchListBox, width=9)
    #SearchListBox.bind(("<<ComboboxSelected"))
    SearchListBox.insert(1, "주제분류")
    # SearchListBox.insert(2,"강의이름")
    # SearchListBox.insert(3,"교수이름")
    # SearchListBox.insert(4,"제공기관")

    SearchListBox.place(x=30, y=100)


def InitInputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk)
    InputLabel = Entry(g_Tk, font=TempFont, width=20, borderwidth=2, relief='ridge')
    InputLabel.pack()
    InputLabel.place(x=130, y=100)
    # 입력하는 거


def InitSearchButton():
    TempFont = font.Font(g_Tk)
    SearchButton = Button(g_Tk, font=TempFont, text="검색", command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=310, y=97)


def SearchButtonAction():
    global SearchListBox

def InitRenderText():
    global RenderText

    RenderTextScrollbar=Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place()
    RenderText=Text(g_Tk, width=49, height=27, borderwidth=12, relief='ridge',yscrollcommand=RenderTextScrollbar.set)
    RenderText.place()
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack()

    RenderText.configure(state='disabled')





InitTopText()
InitSearchListBox()
InitInputLabel()
InitSearchButton()
InitRenderText()
g_Tk.mainloop()
