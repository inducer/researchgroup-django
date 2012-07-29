import os
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"



from treebuilder import TreeBuilderParser

tbp = TreeBuilderParser()
tbp.feed(open("reports.html").read())

from researchgroup.models import Report, ReportFile
from os.path import join, split

for rep in tbp.root().get_all("tr"):
    title = rep["th",0]["p", 0].gobble_text()
    authors = rep["th",0]["p", 1].gobble_text()
    id = rep["td",0].gobble_text()
    year = id.split("-")[0]
    number = int(id.split("-")[1])
    pages = int(rep["td",1].gobble_text().split()[0])
    files = [
            dict(rfile["a",0].Attributes)["href"]
            for rfile in rep["td",2].get_all("div")]
        
    obj = Report(year=year, number=number, title=title,
            authors=authors, pages=pages)
    obj.save()
    for f in files:
        content = open(join("..", "static", f)).read()
        if f.endswith("pdf"):
            descr = "pdf"
        elif f.endswith("ps.gz"):
            descr = "ps.gz"
        else:
            raise RuntimeError
        fname = split(f)[1]

        fobj = ReportFile(description=descr, report=obj)
        fobj.save_file_file(fname, content)

    print year, number
    print title
    print authors
    print pages
    print files

