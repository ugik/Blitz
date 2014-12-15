from emailahoy import VerifyEmail
import xlrd
import xlwt
workbook = xlrd.open_workbook('scrape-Ideafit.xls')
worksheet = workbook.sheet_by_name('Trainers')

def variants(first_name, last_name, variant):
    if variant == 0:
        return first_name+'.'+last_name                     # john.smith@
    elif variant == 1:
        return first_name[0]+last_name                      # jsmith@
    elif variant == 2:
        return first_name[0]+'.'+last_name                  # j.smith@
    elif variant == 3:
        return first_name[0]+last_name[0]                   # js@
    elif variant == 4:
        return 'info'                                       # info@
    else:
        return ""

def verify(mail):
    e = VerifyEmail()
    status = e.verify_email_smtp(
                        email=str(mail),
                        from_host='mydomain.com',
                        from_email='verify@mydomain.com'
                    )

    return status[0]    # return of 250 is valid address

verify('gk@blitz.us')
exit

emails = []
num_rows = worksheet.nrows - 1
curr_row = 0
#while curr_row < num_rows:
while curr_row < 100:
    curr_row += 1
    row = worksheet.row(curr_row)
    first_name = worksheet.cell_value(curr_row, 0).split(' ')[0]
    last_name = worksheet.cell_value(curr_row, 0).split(' ')[1]
    url = worksheet.cell_value(curr_row, 3)
    website = url[url.rfind('.',0,len(url)-6)+1:]
    print curr_row, first_name, last_name, website

    matches = []
    for t in range(5):
        v = variants(first_name, last_name, t)+"@"+website
        validate = verify(v)
        if validate == 250:
            matches.append({'name': worksheet.cell_value(curr_row, 0), 'website': website, 'email': v})

    if len(matches) < 5:   # only save it if not all match (false positive)
        for match in matches:
            emails.append(match)
            print match['email']


workbook = xlwt.Workbook()
sheet = workbook.add_sheet("Trainers")

for i,email in enumerate(emails):
    sheet.write(i, 0, email['name'])
    sheet.write(i, 1, email['website'])
    sheet.write(i, 2, email['email'])

workbook.save("Ideafit-emails.xls")

