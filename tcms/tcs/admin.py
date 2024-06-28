from django.contrib import admin
from .models import File, TCS ,Project

admin.site.register(File)
admin.site.register(TCS)
admin.site.register(Project)

from django.contrib import admin

# Set the header for the admin site
admin.site.site_header = "TCMS"

# Set the title for the admin site
admin.site.site_title = "TCMS"

# Set the index title for the admin site
admin.site.index_title = "Welcome to TCMS Admin Dashboard"

