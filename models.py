from django.db import models

class RakuRecipeCategoryLarge(models.Model):
    category_id = models.IntegerField(default=0,unique=True)
    category_name = models.CharField(max_length=50,blank=True,null=True)
    category_url = models.CharField(max_length=255,blank=True,null=True)

class RakuRecipeCategoryMedium(models.Model):
    category_id = models.IntegerField(default=0,unique=True)
    category_name = models.CharField(max_length=50,blank=True,null=True)
    category_url = models.CharField(max_length=255,blank=True,null=True)
    parent_category_id = models.IntegerField(default=0)

class RakuRecipeCategorySmall(models.Model):
    category_id = models.IntegerField(default=0,unique=True)
    category_name = models.CharField(max_length=50,blank=True,null=True)
    category_url = models.CharField(max_length=255,blank=True,null=True)
    parent_category_id = models.IntegerField(default=0)

class RakuRecipeMenu(models.Model):
    food_image_url = models.CharField(max_length=255,blank=True,null=True)
    medium_image_url = models.CharField(max_length=255,blank=True,null=True)
    nickname = models.CharField(max_length=255,blank=True,null=True)
    pickup = models.CharField(max_length=50,blank=True,null=True)
    rank = models.CharField(max_length=50,blank=True,null=True)
    recipe_cost = models.CharField(max_length=50,blank=True,null=True)
    recipe_description = models.CharField(max_length=255,blank=True,null=True)
    recipe_id = models.CharField(max_length=50,blank=True,null=True)
    recipe_indication = models.CharField(max_length=50,blank=True,null=True)
    recipe_material = models.JSONField()
    recipe_publishday = models.CharField(max_length=50,blank=True,null=True)
    recipe_title = models.CharField(max_length=200,blank=True,null=True)
    recipe_url = models.CharField(max_length=255,blank=True,null=True)
    shop = models.CharField(max_length=50,blank=True,null=True)
    small_image_url = models.CharField(max_length=255,blank=True,null=True)
    large_category_id = models.ForeignKey(RakuRecipeCategoryLarge,on_delete=models.CASCADE,null=True,blank=True,related_name="large_category_data",to_field="category_id")
    medium_category_id = models.ForeignKey(RakuRecipeCategoryMedium,on_delete=models.CASCADE,null=True,blank=True,related_name="medium_category_data",to_field="category_id")
    small_category_id = models.ForeignKey(RakuRecipeCategorySmall,on_delete=models.CASCADE,null=True,blank=True,related_name="small_category_data",to_field="category_id")
    recipe_category_id = models.CharField(max_length=50,blank=True,null=True)
    favorite_flag = models.BooleanField(default=False)

