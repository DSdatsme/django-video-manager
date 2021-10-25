from django.db import models
from django.db.models.fields import DecimalField
from django.http import Http404


class Video(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=56, blank=False)
    size = models.BigIntegerField(blank=False, default=0)
    path = models.CharField(max_length=120, blank=False, default='')
    duration = models.DecimalField(
        max_digits=20, decimal_places=3, default=DecimalField(0.000))
    codec = models.CharField(max_length=120, blank=False, default='')
    container = models.CharField(max_length=120, blank=False, default='')



def get_video_by_id(video_id):
    try:
        required_video = Video.objects.get(id=video_id)
        return required_video
    except Video.DoesNotExist:
        raise Http404("Video does not exist")
