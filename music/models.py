from django.db import models

class DeleteModel(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_deleted=False)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    class Meta:
        abstract = True
    objects = DeleteModel()

    def delete(self,*args, **kwargs):
        self.is_deleted = True
        self.save(*args,**kwargs)




class Author(BaseModel):
    full_name = models.CharField(max_length=100,default='')
    birthday = models.DateField()
    country = models.CharField(max_length=100,default='')
    image = models.ImageField(upload_to='author_images/', null=True, blank=True)



    def __str__(self):
        return self.full_name


class Music(BaseModel):
    genre = models.CharField(max_length=100)
    text = models.TextField()
    published_year = models.DateField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
    audio = models.FileField(upload_to='music_audios/', null=True, blank=True)



    def __str__(self):
        return f"{self.genre} - {self.published_year}"



