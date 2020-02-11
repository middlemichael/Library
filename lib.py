from bs4 import BeautifulSoup
import requests
import re
import math
import sys
import ebook
import os

#Create subfolders
if not os.path.exists('Books'):
    os.makedirs('Books')
    os.makedirs('Books/Kindle')

def results(link):
#turn search query into beautiful soup, returns how many results and pages
    r = requests.get(link)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    file_count = soup.find_all('td')[2].text
    pages = math.ceil(int(re.findall(r'\d+', file_count[0:10])[0])/50)
    print("\n",file_count, "\n" ,pages,"pages. Hit Enter to view next page.\n")

def pages(link):
#return how many pages
    r = requests.get(link)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    file_count = soup.find_all('td')[2].text
    pages = math.ceil(int(re.findall(r'\d+', file_count[0:10])[0])/50)
    return pages    

def search(link):
#returns search results from 1-50 on a given page
    r = requests.get(link)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    try:
        v=-6
        w=-4
        x=-35
        y=-32
        z = 0
        while x and y < 2115:
            v += 43
            w += 43 
            x += 43 
            y += 43 
            z += 1
            title = soup.find_all('td')[x]
            author = soup.find_all('td')[y]
            ext = soup.find_all('td')[w]
            size = soup.find_all('td')[v]
            print(z, author.text,"-",title.text,"-",ext.text,size.text)
    except IndexError:
        print("\nEnd of results")

#set counter to know which page it is currently on
counter = 1
page = "https://libgen.is/search.php?&res=50&req=" + input("search: ").replace(" ", "+") + "&phrase=1&view=detailed&column=def&sort=def&sortmode=ASC&page=1"
results(page)
search(page)


while True:
#run the code. takes input as number only. if 0, breakout and convert, otherswise if num in range of books, download selected book.
    try:
        ans = int(input("\nSelect Book Number, or type 0 to run convert: "))
        if ans == 1:
            x = 8
            y = 11
            z = 39
            if counter == 1:
                r = requests.get(page)
                html = r.text
                soup = BeautifulSoup(html, 'lxml')
            else:
                r = requests.get(nextpage)
                html = r.text
                soup = BeautifulSoup(html, 'lxml')
        elif ans > 1 and ans < 51:
            x = ans*43+8-43
            y = ans*43+11-43
            z = ans*43+39-43
            if counter == 1:
                r = requests.get(page)
                html = r.text
                soup = BeautifulSoup(html, 'lxml')
            else:
                r = requests.get(nextpage)
                html = r.text
                soup = BeautifulSoup(html, 'lxml')            
        elif ans == 0:
            break
    except ValueError:
            print("Next page results\n")
            counter = counter + 1
            if counter <= pages(page):
                nextpage = page[:-1]+str(counter)
                search(nextpage)
                continue                
            else:
                print("No more Pages. Type 0 to exit.")
                continue

#get book and handle download showing progress bar
    get_book = "http://93.174.95.29/_ads/"+' '.join(map(str,soup.find_all("td")[x]('a')))[31:63]
    link =soup.find_all('td')[x].text," - ",soup.find_all('td')[y].text,".",soup.find_all('td')[z].text
    book = "".join(link)
    print(book)
    dl = requests.get("http://93.174.95.29"+BeautifulSoup(requests.get(get_book).text, 'lxml').find("a").get("href"))
    url = "http://93.174.95.29"+BeautifulSoup(requests.get(get_book).text,'lxml').find("a").get("href")
    with open("Books/"+book, 'wb') as f:
        response = requests.get(url, stream=True)
        total = response.headers.get('content-length')
        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/125), 128*128)):
                downloaded += len(data)
                f.write(data)
                done = int(50*downloaded/total)
                sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                sys.stdout.flush()
    sys.stdout.write('\n')

#run convert and send to kindle and drive.
print("\nRun Convert\n")
ebook.run_convert()            
ebook.speak_it()
ebook.send_it()


