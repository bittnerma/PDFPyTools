from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from RPPGLib import io
import os
import re
import shutil

current_dir = os.path.dirname(os.path.realpath(__file__))

pdf_files = io.get_all_files_of_type(current_dir,".pdf")

for file in pdf_files:

    fp = open(file, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)

    #print(doc.info)  # The "Info" metadata
    try:
        year = "0000"
        author_part = "nbdy"
        title_part = "nt"
        ctr = 0


        if "Subject" in doc.info[0]:
            subject = doc.info[0]["Subject"].decode()
            year_regex = re.compile(r'\d{4}')
            mo = year_regex.search(subject)

            year = mo.group()
            ctr += 1
            #print(year)
        
        if "Author" in doc.info[0]:
            author_part = doc.info[0]["Author"].decode().split(' ')[-1]
            ctr += 1
            #print(author_part)

        if 'Title' in doc.info[0]:
            title_part = " ".join(doc.info[0]["Title"].decode().split(' ')[:5])
            ctr += 1
            #print(title_part)

        new_name = "%s_%s_%s.pdf" % (year,author_part,title_part)

        #Rename the file if we have at least two of the three things given
        if ctr >= 2:
            fp.close()
            os.rename(file,new_name)
        print(new_name)
        
    except:
        print('Something went wrong with %s' % file)