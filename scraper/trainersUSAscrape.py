from bs4 import BeautifulSoup, SoupStrainer
import urllib2
import re
import xlwt
workbook = xlwt.Workbook()
sheet = workbook.add_sheet("Trainers")

row = 1
for page in range(100, 1200):
    url = "http://www.trainersusa.com/personal-trainer/%s/" % page
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)

    title = soup.title.contents[0]
    name = title[0:title.index('-')]
    text = soup.get_text()
    
    if "This Profile is Unavailable" in text:
        pass
    else:
        sheet.write(row, 0, name)
        phone = ''        
        try:
            phone = text[text.index('email me')+12:text.index('email me')+26]
            sheet.write(row, 1, phone)
        except:
            pass

        print page, name, phone

    row += 1

workbook.save("scrape-trainersUSA.xls")

# <codecell>

workbook.save("scrape-trainersUSA.xls")

