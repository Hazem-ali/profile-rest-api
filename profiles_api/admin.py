from django.contrib import admin
from django.db import models

from profiles_api import models

# Register your models here.

# makes userprofile accessible on admin interface
admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)