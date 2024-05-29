from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pretty_html_table import build_table
from smtplib import SMTP
import os
from datetime import datetime
import xml.etree.ElementTree as ET



SENDER_MAIL = "automationmail92@gmail.com"
SENDER_PWD = "***********"
Tester = "sachin@primeqasolutions.com"
cc = os.environ.get(
    "EMAIL_CC", "sachin@primeqasolutions.com"
)
Recipents = cc.split(",") + [Tester]



def fetch():
    path = os.getcwd() + "\\junit.xml"
    tree = ET.parse(path)
    root = tree.getroot()
    test_results = []
    for testcase in root.findall('.//testcase'):
        test_classname = testcase.get('classname')
        test_name = testcase.get('name')
        time_taken = testcase.get('time')
        error_message = None
        failure = testcase.find('failure')
        if failure is not None:
            error_message = failure.get('message')
        if error_message:
            test_results.append([test_classname,test_name, "Fail" , time_taken, error_message])
        else:
            test_results.append([test_classname,test_name, "Pass", time_taken])
    # return test_results
    print(test_results)
    return test_results

def Send_Mail():
    print("Sending Mail...........")
    message = MIMEMultipart()
    message["Subject"] = "Automation report " + str(
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )
    message["From"] = SENDER_MAIL
    message["To"] = Tester
    message["Cc"] = cc
    # style='height: 500px; overflow: auto; width: fit-content'
    html = (
        """\
    	<html>
    	  <head></head>
    	  <body>
    	    <p>Hi,<br>
    	        Please find below Report for Automation Testing
    	    </p>
            <p><a href="""
        + "https://app.11automation.com/"
        + """>Login here with your credentials</a> to check the detailed report</p>
    	    
    	    <p>THIS IS SYSTEM GENERATED MAIL.</p>
    	    <p></p>
    	  </body>
    	</html>
    	"""
    )

    part2 = MIMEText(html, "html")
    message.attach(part2)
    filename = os.path.join(os.getcwd(), "pytest.log")
    attachment = open(filename, "rb")
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment; filename= Logs")
    message.attach(part)

    msg_body = message.as_string()
    try:
        server = SMTP("smtp.gmail.com", 587)
        # outlook = client.Dispatch("Outlook.Application")
        server.starttls()
        server.login(message["From"], SENDER_PWD)
        server.sendmail(message["From"], Recipents, msg_body)
        server.quit()
        print("Mail Sent successfully")
    except Exception as e_mail:
        print("Mail sending Failed")
        print(e_mail)
