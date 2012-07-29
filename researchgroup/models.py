from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField

class PersonCategory(models.Model):
    name = models.CharField("category", max_length=200, blank=True)
    sort_weight = models.IntegerField("sort weight", default=0)
    can_advise = models.BooleanField()
    can_invite = models.BooleanField()

    class Meta:
        verbose_name_plural = "people categories"
        ordering = ["sort_weight"]

    def __unicode__(self):
        return self.name

class Person(models.Model):
    active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=200, blank=True)
    middle_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True)
    pcat = models.ForeignKey(PersonCategory, verbose_name="category")
    email = models.EmailField(blank=True)
    homepage = models.URLField(blank=True, verify_exists=False)
    office_phone = PhoneNumberField(blank=True)
    home_phone = PhoneNumberField(blank=True)
    research_area = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(blank=True, upload_to="people_photos")
    advisors = models.ManyToManyField("self", blank=True,
            limit_choices_to={'pcat__can_advise__exact': True},
            symmetrical=False)
    graduation_year = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "people"
        ordering = ['last_name']

    def __unicode__(self):
        names = [self.first_name]
        if self.middle_name:
            names.append(self.middle_name)
        names.append(self.last_name)
        return u" ".join(names)

class SeminarTalk(models.Model):
    time = models.DateTimeField()
    speaker = models.CharField(max_length=200)
    speaker_affiliation = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200)
    invited_by = models.ForeignKey(Person, blank=True, null=True,
            limit_choices_to={'pcat__can_invite__exact': True},
            )
    title = models.CharField(max_length=200, blank=True)
    notes = models.CharField(max_length=200, blank=True)
    speaker_homepage = models.URLField("homepage", blank=True)
    abstract = models.TextField(blank=True)
    slides = models.FileField(blank=True, upload_to="seminar_slides")

    class Meta:
        ordering = ['-time']

    def __unicode__(self):
        return u"%s on %s" % (self.speaker, str(self.time.date()))

class Class(models.Model):
    department = models.CharField(max_length=6)
    number = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    abstract = models.TextField(blank=True)
    prerequisites = models.CharField(max_length=200, blank=True)
    webpage = models.URLField("class homepage", blank=True)

    class Meta:
        verbose_name_plural = "classes"
        ordering = ['department', 'number']

    def __unicode__(self):
        return "%s%s - %s" % (self.department, self.number, self.title)

class Report(models.Model):
    year = models.IntegerField()
    number = models.IntegerField()
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    abstract = models.TextField(blank=True)
    pages = models.IntegerField()
    date = models.DateField()

    class Meta:
        ordering = ['-year', '-number']

    def __unicode__(self):
        return "%d-%d: %s" % (self.year, self.number, self.title)

class ReportFile(models.Model):
    description = models.CharField(max_length=30)
    file = models.FileField(blank=True, upload_to="report_files")
    report = models.ForeignKey(Report)

    def __unicode__(self):
        return "%s (%s)" % (self.description, self.report)

class NewsItem(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Person, null=True)
    lead_text = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    start_showing = models.DateField(blank=True, null=True)
    stop_showing = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return self.title

class RotationImageType(models.Model):
    name = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class RotationImage(models.Model):
    caption = models.CharField(max_length=200)
    image = models.ImageField(upload_to="rotation_images")
    type = models.ForeignKey(RotationImageType)

    class Meta:
        ordering = ['caption']

    def __unicode__(self):
        return self.caption

class StaticPage(models.Model):
    address = models.CharField(max_length=200, help_text="For example: research/cem")
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Person)
    html = models.TextField(blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.address, self.title)

