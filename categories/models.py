# from django.db import models
# # from django.urls import reverse

# # Create your models here.
# class Category(models.Model):
#     category_name = models.CharField(max_length=50,unique=True)
#     category_image=models.ImageField(upload_to='photos/categories/')
#     description = models.TextField(max_length=225,blank=True)
#     is_activate=models.BooleanField(default=True)

#     class Meta:
#         verbose_name = 'category'
#         verbose_name_plural= 'categories'

#     # def get_url(self):
#     #     return reverse('products_by_category', args={self.slug})
    
#     def __str__(self):
#         return self.category_name
    

#     # other fields...

# class SubCategory(models.Model):
#     # Fields for SubCategory model
#     pass

# class Sub_Category(models.Model):
#     sub_category_name = models.CharField(max_length=50,unique=True)
#     sub_category_description=models.TextField(max_length=225,blank=False,default=None)
#     sub_Category_image=models.ImageField(upload_to='photos/sub_categories/',blank=False,default=None)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     is_activate=models.BooleanField(default=True)

#     class Meta:
#         verbose_name = 'sub category'
#         verbose_name_plural = 'sub categories'

#     # def get_url(self):
#     #     return reverse('products_by_sub_category',args=[self.slug])

#     def __str__(self):
#         return self.sub_category_name


from django.db import models
from django.urls import reverse




# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    category_image=models.ImageField(upload_to='photos/categories/')
    description = models.TextField(max_length=225,blank=True)
    is_activate=models.BooleanField(default=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural= 'categories'

    def get_url(self):
        return reverse('products_by_category', args={self.slug})
    

    def __str__(self):
        return self.category_name
    
class Sub_Category(models.Model):
    sub_category_name = models.CharField(max_length=50,unique=True)
    sub_category_description=models.TextField(max_length=225,blank=False,default=None)
    sub_Category_image=models.ImageField(upload_to='photos/sub_categories/',blank=False,default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_activate=models.BooleanField(default=True)
    

    class Meta:
        verbose_name = 'sub category'
        verbose_name_plural = 'sub categories'

    def get_url(self):
        return reverse('products_by_sub_category',args=[self.slug])

    def __str__(self):
        return self.sub_category_name
    
    
    