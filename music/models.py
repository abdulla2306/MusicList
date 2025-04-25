from django.db import models


class Author(models.Model):
    full_name=models.CharField(max_length=255)
    birthday=models.DateField()
    country=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.full_name


from django.db import models


class Music(models.Model):
    genre = models.CharField(max_length=100)
    text = models.TextField()
    published_year = models.DateField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)  # Bu satrni qo'shing
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.genre} - {self.published_year}"

