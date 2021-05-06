from django.contrib import admin

# Register your models here.
from parserav.models import Job

class JobAdmin(admin.ModelAdmin):
    list_display=("title", "location", "price", "telephone")


    class Meta:
        model=Job


admin.site.register(Job, JobAdmin)