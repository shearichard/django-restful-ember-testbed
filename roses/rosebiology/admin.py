from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Reference
from .models import Image 
from .models import CommonName 
from .models import Use 
from .models import Subspecies 
from .models import Range 
from .models import Species
from .models import UserProfile

admin.site.register(Reference)
admin.site.register(Image)
admin.site.register(CommonName)
admin.site.register(Use)
admin.site.register(Subspecies)
admin.site.register(Range)
admin.site.register(Species)
admin.site.register(UserProfile)
