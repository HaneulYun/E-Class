import mimetypes
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

#global value
host = "smtp.gmail.com" # Gmail STMP 서버 주소.
port = "587"


def MakeHtmlDoc(bookMark_List):
    from xml.dom.minidom import getDOMImplementation
    impl = getDOMImplementation()
    newdoc = impl.createDocument(None, "html", None)  # DOM 객체 생성
    top_element = newdoc.documentElement
    header = newdoc.createElement('header')
    top_element.appendChild(header)

    # Body 엘리먼트 생성.
    body = newdoc.createElement('body')

    for item in bookMark_List:
        b = newdoc.createElement('b')
        # create text node
        ibsnText = newdoc.createTextNode("확인")  # < 병원명 >
        b.appendChild(ibsnText)

        body.appendChild(b)

    top_element.appendChild(body)

    return newdoc.toxml()


# 메일을 발송한다.
def sendmail(addr, html):
    global host,port
    senderAddr = "hello3o456@gmail.com"
    recipientAddr = addr
    msgtext=''

    msg = MIMEBase('multipart','alternative')

    msg['Subject']="하늘이 바보"
    msg['From']=senderAddr
    msg['To']=recipientAddr

    HtmlPart = MIMEText(html, 'html', _charset='UTF-8')

    msg.attach(HtmlPart)

    s = smtplib.SMTP(host, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("hello3o456@gmail.com","dkssud110112")

    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()

