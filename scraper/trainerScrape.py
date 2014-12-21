from bs4 import BeautifulSoup, SoupStrainer
import urllib2
import re
import xlwt
import sys

if len(sys.argv)>0:
    DELTA=int(sys.argv[1])
else:
    DELTA=1
print "DELTA: "+str(DELTA)

workbook = xlwt.Workbook()
sheet = workbook.add_sheet("Trainers")

list = []
row = 0
for page in range(DELTA, DELTA+99):
    print "===================================================== Page %s" % page
    url = "http://www.ideafit.com/find-personal-trainer/ma/winchester?page=%s&country=us&zip=01890&location=01890&distance=2500&specialty[4202]=4202&specialty[4205]=4205&specialty[4207]=4207&specialty[4210]=4210&specialty[4225]=4225&specialty[4241]=4241&specialty[4246]=4246" % page
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    trainers = soup.findAll(attrs={"class" : "fc-search-result"})
    for trainer in trainers:
        piece = trainer.findAll(attrs={"class" : "title"})[0].contents[1]
        print trainer.findAll(attrs={"class" : "title"})[0].contents[1].string + " - " +piece['href']
        t = {"name": trainer.findAll(attrs={"class" : "title"})[0].contents[1].string, "href": piece['href']}

        if not [element for element in list if element['name'] == t['name']]:
            list.append(t)
        
    for t in range(0, len(list)):
        url = "http://www.ideafit.com"+list[t]['href']
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content)
#        print soup.title.contents[0]
        sheet.write(row, 0, list[t]['name'])

        try:
            loc = soup.findAll(attrs={"class" : "user-citystatezip"})[0].contents[0]
            sheet.write(row, 1, loc)
#            print loc
        except:
            pass
        try:
            web = soup.findAll(attrs={"class" : "user-website"})[0].a['href']
            sheet.write(row, 2, xlwt.Formula('HYPERLINK("'+web+'"; "'+web+'")'))
#            print web
        except:
            pass
        try:
            tweet = soup.findAll(attrs={"class" : "latest-tweet"})[0].div.a['href']
            sheet.write(row, 3, xlwt.Formula('HYPERLINK("'+tweet+'"; "'+tweet+'")'))
#            print "Twitter: "+tweet
        except:
            pass 
        row += 1
    
    list = []
    
workbook.save("scrape-Ideafit-"+str(DELTA)+".xls")

