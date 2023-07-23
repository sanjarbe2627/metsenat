from django.contrib import admin

from senat.models import Sponsor, Student, University, Sponsorship

admin.site.register(Sponsor)
admin.site.register(Student)
admin.site.register(University)
admin.site.register(Sponsorship)
