from django import template

register = template.Library()

def scramblemail(email):
    import scg.settings
    from django.utils.safestring import mark_safe
    return mark_safe(
            email.replace("@", "<img src=\"%simages/at.gif\"/>" 
                % scg.settings.STATICSITE_ROOT))
register.filter('scramblemail', scramblemail)

