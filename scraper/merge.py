import xlrd, xlwt
import glob, os.path

def merge_xls (in_dir="./", out_file="merged_output.xls"):

    xls_files   = glob.glob(in_dir + "*.xls")
    sheet_names = [os.path.basename(v)[:-4] for v in xls_files]
    sheet_excl  = [os.path.basename(v)[:-4] for v in xls_files if
len(os.path.basename(v)[:-4]) > 29]
    merged_book = xlwt.Workbook()

    if in_dir[-1:] != "/": in_dir = in_dir + "/"
    xls_files.sort()
    if xls_files:
        for k, xls_file in enumerate(xls_files):
            print "---> Processing file %s" % (xls_file)
            if len (sheet_names[k]) <= 29:
                book = xlrd.open_workbook(xls_file)
                if book.nsheets == 1:
                    ws    = merged_book.add_sheet(sheet_names[k])
                    sheet = book.sheet_by_index(0)
                    for rx in range(sheet.nrows):
                        for cx in range(sheet.ncols):
                            ws.write(rx, cx, sheet.cell_value(rx, cx))
                elif book.nsheets in range(2, 100):
                    for sheetx in range(book.nsheets):
                        sheet0n = sheet_names[k]+str(sheetx+1).zfill(2)
                        ws      = merged_book.add_sheet(sheet0n)
                        sheet   = book.sheet_by_index(sheetx)
                        for rx in range(sheet.nrows):
                            for cx in range(sheet.ncols):
                                ws.write(rx, cx, sheet.cell_value(rx, cx))
                else:
                    print "ERROR *** File %s has %s sheets (maximum is 99)"
% (xls_file, book.nsheets)
                    raise
            else:
                print "WARNING *** File name too long: <%s.xls> (maximum is
29 chars) " % (sheet_names[k])
                print "WARNING *** File <%s.xls> was skipped." %
(sheet_names[k])
        merged_book.save(out_file)
        print
        print "---> Merged xls file written to %s using the following source
files: " % (out_file)
        for k, v in enumerate(sheet_names):
            if len(v) <= 29:
                print "\t", str(k+1).zfill(3), "%s.xls" % (v)
        print
        if sheet_excl:
            print "--> The following files were skipped because the file
name exceeds 29 characters: "
            for k, v in enumerate(sheet_excl):
                print "\t", str(k+1).zfill(3), v
    else:
        print "NOTE *** No xls files in %s. Nothing to do." % (in_dir)

