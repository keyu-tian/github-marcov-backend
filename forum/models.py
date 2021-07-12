from django.db import models
from user.models import User


class Question(models.Model):
    title = models.CharField(verbose_name='标题', max_length=512)
    content = models.TextField(verbose_name='内容')
    views = models.IntegerField(verbose_name='浏览量', default=0)
    user = models.ForeignKey(to=User, related_name='published_question', on_delete=models.CASCADE, verbose_name='发布者')
    published_time = models.CharField(verbose_name='发布时间', max_length=32)
    replied_time = models.CharField(verbose_name='最近回复时间', max_length=32, blank=True, null=True)
    expert_reply = models.BooleanField(verbose_name='是否有专家回复', default=False)
    solved = models.BooleanField(verbose_name='是否被解决', default=False)


class Content(models.Model):
    replied_content = models.ForeignKey('self', related_name='all_reply_content', on_delete=models.CASCADE, verbose_name='回复的内容', blank=True, null=True)
    question = models.ForeignKey(to=Question, related_name='question_all_content', on_delete=models.CASCADE, verbose_name='对应的问题')
    user = models.ForeignKey(to=User, related_name='published_content', on_delete=models.CASCADE, verbose_name='发布者')
    published_time = models.CharField(verbose_name='发布时间', max_length=32)
    is_top = models.BooleanField(verbose_name='是否被置顶', default=False)
    content = models.TextField(verbose_name='内容')


class Tag(models.Model):
    name = models.CharField(verbose_name='标签名', max_length=512)
    question = models.ForeignKey(to=Question, related_name='question_all_tag', on_delete=models.CASCADE, verbose_name='对应的问题')

