import mimetypes
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

#global value
host = "smtp.gmail.com" # Gmail STMP 서버 주소.
port = "587"

def MakeHtmlDoc(self):
    from xml.dom.minidom import getDOMImplementation
    impl = getDOMImplementation()
    newdoc = impl.createDocument(None, "html", None)  # DOM 객체 생성
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    # Body 엘리먼트 생성.
    body = newdoc.createElement('body')

    body.appendChild(newdoc.createTextNode('총 {} 개의 강의 정보를 수신하였습니다.\n'.format(self.books.__len__())))
    body.appendChild(newdoc.createElement('br'))
    body.appendChild(newdoc.createElement('br'))
    body.appendChild(newdoc.createElement('br'))

    for d in self.books:
        body.appendChild(newdoc.createTextNode('강의이름 : {}'.format(d['course_title'])))
        body.appendChild(newdoc.createElement('br'))
        body.appendChild(newdoc.createTextNode('....제공기관 : {}'.format(d['provider'])))
        body.appendChild(newdoc.createElement('br'))
        body.appendChild(newdoc.createTextNode('....교수자명 : {}'.format(d['lecturer'])))
        body.appendChild(newdoc.createElement('br'))
        body.appendChild(newdoc.createTextNode('....강의링크 : {}'.format(d['course_url'])))
        body.appendChild(newdoc.createElement('br'))
        body.appendChild(newdoc.createElement('br'))

    top_element.appendChild(body)

    return newdoc.toxml()


# 메일을 발송한다.
def sendmail(addr, html):
    global host,port
    senderAddr = "hello3o456@gmail.com"
    recipientAddr = addr
    msgtext=''

    msg = MIMEBase('multipart','alternative')

    msg['Subject']="[E-Class(공개강의 검색 엔진)] 북마크 목록을 전송해드립니다."
    msg['From']=senderAddr
    msg['To']=recipientAddr

    HtmlPart = MIMEText(html, 'html', _charset='UTF-8')

    msg.attach(HtmlPart)

    print("connect smtp server ... ")
    s = smtplib.SMTP(host, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("hello3o456@gmail.com","dkssud110112")
    try:
        s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    except:
        print("사망각")
        s.close()
        return False
    else:
        print("Mail sending complete!!!")
        s.close()
        return True
