import subprocess
import os
from pathlib import Path
import json
import requests
import drive


def book_shelf():

    books = []
    for filename in os.listdir("Books/"):
        if filename.endswith(".epub"):
            epub = filename[:-len(".epub")]
            books.append(epub)
        elif filename.endswith(".rar"):
            rar = filename[:-len(".rar")]
            books.append(rar)
        elif filename.endswith(".mobi"):
            mobi = filename[:-len(".mobi")]
            books.append(mobi)
        elif filename.endswith(".pdf"):
            pdf = filename[:-len(".pdf")]
            books.append(pdf)
        elif filename.endswith(".html"):
            html = filename[:-len(".html")]
            books.append(html)
        else:
            pass            
    return len(books)   

def book():
    files = []
    for filename in os.listdir("Books/"):
        if filename.endswith(".epub"):
            epub = filename
            files.append(epub)           
        elif filename.endswith(".rar"):
            rar = filename
            files.append(rar)           
        elif filename.endswith(".mobi"):
            mobi = filename
            files.append(mobi)
        elif filename.endswith(".pdf"):
            pdf = filename
            files.append(pdf)
        elif filename.endswith(".html"):
            html = filename
            files.append(html)
    while len(files) > 0:
        return files[0]
    else:
        files = "Empty"
        return files

def convert():
#Converts the chosen book to the correct file, deletes the orignal file and places the now .mobi file into a subfolder.
#The book is now ready to be sent
    call = '/Applications/calibre.app/Contents/MacOS/ebook-convert '  
    call = "ebook-convert" 
    folder_out = ("Books/Kindle/")  
    for files in book():
        if book() == "Empty":
            return book()
        else:
            book_in = "Books/" + book()
            book_out = "Books/Kindle/" + book()[:-5] + (".mobi")
            book_out2 = "Books/Kindle/" + book()[:-5] + (".epub")
            final = call + " '" + book_in + "' '" + book_out + "' "
            final2 = call + " '" + book_in + "' '" + book_out2 + "' "
            os.system(final)   
            print("\n", book(),"Converted Mobi")            
            os.system(final2)
            os.remove(book_in)
def run_convert():
#Loops the convert process until there are no more books to convert.
    while book_shelf() > 0:
        convert()
        continue
        if book_shelf() == 0:
            break
    else:
        print("Sending Files to Kindle. \n")

def first_send():
#Returns a book ready to be sent, if there is no book, returns nothing.
    send = []
    for mobi in os.listdir("Books/Kindle/"):
        if mobi.endswith(".mobi"):
            send.append(mobi)
        else:
            pass
    for file in os.listdir("Books/Kindle/"):
        if file != file.endswith(".mobi"):
            send.append("No Mobis Found")          
    return send[0]

def second_send():
#Returns a book ready to be sent, if there is no book, returns nothing. epub version
    send = []
    for epub in os.listdir("Books/Kindle/"):
        if epub.endswith(".epub"):
            send.append(epub)
        else:
            pass
    return send[0]

def send_to_reader():
#sends book to drive
    headers = {"Authorization": ("Bearer " + drive.accesstoken())}
    para = {"name": second_send(), "parents": ["INPUT HERE"]}
    files = {'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'), 'file': open("Books/Kindle/" + second_send(), "rb") }
    r = requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart", headers=headers, files=files )  
    print(r.text)
    os.remove("Books/Kindle/" + second_send())

def send_to_kindle():
#Packages book to email and sends
    print("Sending " + first_send() + " to Kindle.")
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    import os.path
    email = 'YOUR NEW GMAIL ADDRESS'
    password = 'YOUR NEW GMAIL PASSWORD'
    send_to_email = "YOUR KINDLE EMAIL"
    subject = first_send()
    message = first_send() + (" Sent to Kindle")
    file_location = 'Books/kindle/' + first_send()
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    # Setup the attachment
    filename = os.path.basename(file_location)
    attachment = open(file_location, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    # Attach the attachment to the MIMEMultipart object
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()   
    print("Sent\n")
    #Remove file from folder
    os.remove(file_location)

def booklist():
#Returns value of books to send. if value = 0, will not send anything
    shelf = []
    for filename in os.listdir("Books/Kindle/"):
        if filename.endswith(".mobi"):
            mobi = filename[:-len(".mobi")]
            shelf.append(mobi)
        else:
            pass        
    return len(shelf)

def booklist2():
#Returns value of books to send. if value = 0, will not send anything
    shelf = []
    for filename in os.listdir("Books/Kindle/"):
        if filename.endswith(".epub"):
            epub = filename[:-len(".epub")]
            shelf.append(epub)
        else:
            pass        
    return len(shelf)

def send_it():
#if there are books to send, the process will loop until all are sent.
    while booklist() > 0:
        send_to_kindle()
        continue
        if booklist() == 0:
            break
    else:
        pass

def speak_it():
#if there are books to send, the process will loop until all are sent.
    while booklist2() > 0:
        print("Sending " + second_send() + " to Drive")
        send_to_reader()
        continue
    if booklist() == 0:
        pass


