from django.contrib import admin
from models import \
        PersonCategory, \
        Person, \
        SeminarTalk, \
        Class, \
        ReportFile, \
        Report, \
        NewsItem, \
        RotationImageType, \
        RotationImage, \
        StaticPage

class PersonCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort_weight')

admin.site.register(PersonCategory, PersonCategoryAdmin)

class PersonAdmin(admin.ModelAdmin):
    list_filter = ('pcat', 'active')
    list_display = ('last_name', 'first_name', 'pcat', 'email', 'active')
    search_fields = ('last_name', 'first_name')
    save_on_top = True

admin.site.register(Person, PersonAdmin)

class SeminarTalkAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    search_fields = ('speaker', 'title', 'speaker_affiliation', 'abstract')

admin.site.register(SeminarTalk, SeminarTalkAdmin)

class ClassAdmin(admin.ModelAdmin):
    pass

admin.site.register(Class, ClassAdmin)

class ReportFileInline(admin.StackedInline):
    model = ReportFile
    extra = 3

class ReportAdmin(admin.ModelAdmin):
    list_filter = ('year',)
    search_fields = ('title', 'authors')
    inlines = [ReportFileInline]

admin.site.register(Report, ReportAdmin)

class NewsItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(NewsItem, NewsItemAdmin)

class RotationImageTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(RotationImageType, RotationImageTypeAdmin)

class RotationImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(RotationImage, RotationImageAdmin)

class StaticPageAdmin(admin.ModelAdmin):
    pass

admin.site.register(StaticPage, StaticPageAdmin)


