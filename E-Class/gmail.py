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

    ibsnText = newdoc.createTextNode("확인")  # < 병원명 >
    body.appendChild(ibsnText)

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
