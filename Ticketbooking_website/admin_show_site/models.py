from django.db import models
import datetime



class Movie_details(models.Model):
    name = models.CharField(max_length=100)
    language = models.ManyToManyField("Movie_language")
    duration=models.CharField(max_length=40, null=True)
    genre = models.ManyToManyField('Movie_genre')
    time = models.ForeignKey('Movie_time', on_delete=models.CASCADE,null=True)
    date = models.DateField(default=datetime.date.today,null=True)
    image = models.FileField(upload_to='images')
    trailer = models.CharField(max_length=500, null=True)
    is_active=models.SmallIntegerField(default=1)
    def __str__(self):
        return self.duration
    def __str__(self):
        return self.name


class Movie_time(models.Model):
    time = models.TimeField()

    def __str__(self):
        return self.time.strftime('%I:%M:%p')

class Movie_language(models.Model):
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.language

class Movie_genre(models.Model):
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.genre

# class Movie_date(models.Model):
#     date = models.DateField()

#     def __str__(self):
#         return self.date.strftime("%d/%m/%y")
