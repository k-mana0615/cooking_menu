from django.contrib import admin
from .models import RakuRecipeMenu
from .models import RakuRecipeCategoryLarge
from .models import RakuRecipeCategoryMedium
from .models import RakuRecipeCategorySmall

admin.site.register(RakuRecipeMenu)
admin.site.register(RakuRecipeCategoryLarge)
admin.site.register(RakuRecipeCategoryMedium)
admin.site.register(RakuRecipeCategorySmall)
