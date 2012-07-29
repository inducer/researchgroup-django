import os
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
from datetime import datetime



from treebuilder import TreeBuilderParser

tbp = TreeBuilderParser()
tbp.feed(open("seminars.html").read())

from researchgroup.models import SeminarTalk
from os.path import join, split

for sem in tbp.root().get_all("tr"):
    date = sem["th", 0].gobble_text()
    title = sem["td",1].gobble_text()
    notes = sem["td",2].gobble_text()
    speaker_div = sem["td",0]["div",0]
    assert ("class", "inst") not in speaker_div.Attributes
    speaker = speaker_div.gobble_text()
    speaker_hp = ""
    if speaker_div.count("a"):
        speaker_hp = dict(speaker_div["a",0].Attributes)["href"]
    inst = sem["td",0]["div",1].gobble_text()

    months = {"Jan.":1, "Feb.":2, "Mar.":3, "Apr.": 4, "May":5, "Jun.": 6,
            "Jul.":7, "Aug.":8, "Sept.":9, "Oct.":10, "Nov.":11, "Dec.":12}
    date = date.replace(",", "").split()
    year = int(date[2])
    month = months[date[0]]
    day = int(date[1])
    dt = datetime(year, month, day, 11, 0)

    print dt
    print speaker, speaker_hp
    print inst
    print title
    print notes

    talk = SeminarTalk(time=dt, speaker=speaker, speaker_homepage=speaker_hp,
            speaker_affiliation=inst, title=title, notes=notes,
            location="182 George, Room 002")
    talk.save()

