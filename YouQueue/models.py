from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=50)
    votes = models.IntegerField()
    thumbnail = models.CharField(max_length=200)
    vid = models.CharField(max_length=50)
    sid = models.AutoField(primary_key=True)
    url = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    
    # def __str__(self):
    #     return "SONG: " + title + " with " + str(votes) + " votes."

# python3 manage.py migrate --run-syncdb