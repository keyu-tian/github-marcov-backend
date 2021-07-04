from django.db import models
from utils.cast import encode, decode


# Create your models here.
class News(models.Model):

    title = models.CharField(verbose_name='新闻标题', max_length=255, default='无标题')
    img = models.CharField(verbose_name='图片url', max_length=1024)
    url = models.CharField(verbose_name='新闻url', max_length=1024)
    media = models.CharField(verbose_name='媒体名', max_length=255, default='未知来源')
    publish_time = models.CharField(verbose_name='发布时间', max_length=255, default='未知时间')
    context = models.TextField(verbose_name='新闻内容', max_length=4096, default='无法显示')
