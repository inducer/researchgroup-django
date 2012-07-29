from django.shortcuts import render_to_response
from django.http import Http404
from scg.researchgroup.models import \
  Person, PersonCategory, SeminarTalk, Class, Report, ReportFile, \
  RotationImage, NewsItem, StaticPage
import scg.settings as settings




# tools -----------------------------------------------------------------------
def academic_year(datetime):
    if datetime.month <= 6: 
        return datetime.year - 1
    else: 
        return datetime.year

def random_image(type):
    images = RotationImage.objects.filter(type__name__exact=type)
    if not len(images):
        raise Http404, "no rotation images of type '%s'" % type
    import random
    rng = random.Random()
    rng.seed()
    return images[rng.randrange(len(images))]

def uniq(iterable):
    first = True
    for i in iterable:
        if first or i!= last:
            last = i
            yield i
            first = False




# common stuff ----------------------------------------------------------------
def generate_news(max_news=2, max_seminars=2, sem_past_days=3):
    import datetime
    now = datetime.datetime.now()
    items = []
    from django.db.models import Q
    for item in (NewsItem.objects
            .filter(
            (Q(start_showing__lte=now)|Q(start_showing__isnull=True))&
            (Q(stop_showing__gte=now)|Q(stop_showing__isnull=True)))
            .order_by('-date')[:max_news]):
        item.url = "%snews/%d" % (settings.DYNSITE_ROOT, item.id)
        items.append(item)

    seminar_past_cutoff = now - datetime.timedelta(days=sem_past_days)
    for sem in (SeminarTalk.objects
            .filter(time__gte=seminar_past_cutoff)
            .order_by('time')[:max_seminars]):

        item = NewsItem(date=sem.time.date(), 
                title="Seminar: %s" % sem.speaker,
                author=sem.invited_by,
                abstract=sem.abstract)
        item.url = "%sseminars/%d" % (settings.DYNSITE_ROOT, sem.id)
        items.append(item)

    return items




def common_info():
    pcat_list = PersonCategory.objects.all()
    sem_month_list = list(SeminarTalk.objects.dates("time", "month"))
    sem_month_list.sort()
    sem_month_list.reverse()
    sem_year_list = list(uniq([academic_year(dt) for dt in sem_month_list]))
    rep_year_list = list(uniq([rep.year for rep in Report.objects.all()]))
    class_list = Class.objects.all()

    return {
            "dynsite_root": settings.DYNSITE_ROOT,
            "staticsite_root": settings.STATICSITE_ROOT,
            "pcat_list": pcat_list,
            "sem_year_list": sem_year_list,
            "rep_year_list": rep_year_list,
            "class_list": class_list,
            }




# people stuff ----------------------------------------------------------------
def people(request, person_cat):
    pcat = PersonCategory.objects.get(name__iexact=person_cat)
    objlist = Person.objects.filter(pcat__pk=pcat.id, active=True)
    
    info_dict = common_info()
    info_dict.update(
            {"object_list": objlist, "pcat": pcat}
            )
    return render_to_response("researchgroup/person_list.html", 
            info_dict)




# seminar stuff ---------------------------------------------------------------
def current_seminars(request):
    from datetime import datetime
    return seminars(request, academic_year(datetime.now()))

def seminars(request, year):
    year = int(year)

    seminars = [s for s in SeminarTalk.objects.all() 
            if academic_year(s.time) == year]
    
    info_dict = common_info()
    info_dict.update(
            {"object_list": seminars,
            "sem_year": year}
            )
    return render_to_response("researchgroup/seminar_list.html", 
            info_dict)

def seminar(request, id):
    seminar = SeminarTalk.objects.get(id=id)
    
    info_dict = common_info()
    info_dict.update(
            {"sem": seminar}
            )
    return render_to_response("researchgroup/seminar_detail.html", 
            info_dict)




# reports stuff ---------------------------------------------------------------
def current_reports(request):
    from datetime import datetime
    return reports(request, datetime.now().year)

def reports(request, year):
    query = Report.objects
    if year != "all":
        query = query.filter(year__exact=int(year))
    else:
        query = query.all()

    reports = list(query)
    for rep in reports:
        rep.files = []
        for rfile in ReportFile.objects.filter(report=rep):
            rep.files.append(rfile)

    info_dict = common_info()
    info_dict.update(
            {"object_list": reports, "rep_year": str(year) }
            )
    return render_to_response("researchgroup/report_list.html", 
            info_dict)

def report(request, year, number):
    report = Report.objects.get(year=year, number=number)
    files = ReportFile.objects.filter(report=report.id)

    info_dict = common_info()
    info_dict.update(
            {"rep": report, "rep_files": files }
            )
    return render_to_response("researchgroup/report_detail.html", 
            info_dict)




# minor things ----------------------------------------------------------------
def classes(request):
    return render_to_response("researchgroup/class_list.html", 
            common_info())

def news_detail(request, id):
    item = NewsItem.objects.get(id=id)
    info_dict = common_info()
    info_dict.update({
            "item": item,
            })
    return render_to_response("researchgroup/news_detail.html", 
            info_dict)

def news(request):
    info_dict.update({
            "news_items": generate_news(maxcount=None),
            })
    return render_to_response("researchgroup/news.html", 
            info_dict)

def main_page(request):
    info_dict = common_info()
    info_dict.update({
            "random_image": random_image("main"),
            "news_items": generate_news(),
            })
    return render_to_response("researchgroup/main.html", 
            info_dict)

def handler404(request):
    return render_to_response("404.html", common_info())

def page(request, address):
    from django.template import Template, Context

    ctx = Context(common_info())
    page = StaticPage.objects.get(address=address)
    pagetpl = Template(page.html)

    info_dict = common_info()
    info_dict.update({
            "title": page.title,
            "author": page.author,
            "content": pagetpl.render(ctx),
            })
    return render_to_response("researchgroup/page.html", 
            info_dict)


