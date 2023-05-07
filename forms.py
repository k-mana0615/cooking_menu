from django import forms
from .models import RakuRecipeCategoryLarge
from .models import RakuRecipeCategoryMedium
from .models import RakuRecipeCategorySmall
from .models import RakuRecipeMenu

#class RakuRecipeCategoryLargeForm(forms.ModelForm):
#	class Meta:
#		model = RakuRecipeCategoryLarge
#		fields = ['category_id']
#		widgets = {
#            "category_id": forms.CheckboxSelectMultiple
#        }


#class RakuRecipeCategoryMediumForm(forms.ModelForm):
#	class Meta:
#		model = RakuRecipeCategoryMedium
#		fields = ['category_id','category_name','category_url','parent_category_id']

#class RakuRecipeCategorySmallForm(forms.ModelForm):
#	class Meta:
#		model = RakuRecipeCategorySmall
#		fields = ['category_id','category_name','category_url','parent_category_id']


