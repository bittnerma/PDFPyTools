from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import PDFObjectNotFound
import sys

pages = []

def extract(objid, obj):
    global pages
    if isinstance(obj, dict):
        # 'Type' is PDFObjRef type
        if 'Type' in obj and obj['Type'].name == 'Page':
            pages.append(objid)
        elif 'C' in obj:
            # pr = obj['P']
            # try:
            #     pi = pages.index(pr.objid)+1
            # except:
            #     pi = -1
            # print(objid,pi, obj['Subj'],obj['T'],obj['Contents'])
            if 'Contents' in obj:
                out = obj['Contents'].decode('latin_1').replace('\r|\x84',' ').strip()
                print(out)
        elif 'H' in obj:
            print('Found an H')
                


fp = open("test.pdf", 'rb')
parser = PDFParser(fp)
doc = PDFDocument(parser, "")
visited = set()
for xref in doc.xrefs:
    for objid in xref.get_objids():
        if objid in visited: continue
        visited.add(objid)
        try:
            obj = doc.getobj(objid)
            if obj is None: continue
            extract(objid,obj)
        except(PDFObjectNotFound):
            print(sys.stderr, 'not found:')