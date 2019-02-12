from django.db import models

# Create your models here.

class User(models.Model):
    SEX = (
        ('M', '男性'),
        ('F', '女性'),
        ('S', '保密'),
    )
    nickname = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)
    age = models.IntegerField(default=18)
    sex = models.CharField(max_length=8, choices=SEX)
    icon = models.ImageField()
    plt_icon = models.URLField(default='',verbose_name='第三方平台的头像URL')
    prem_id = models.IntegerField()

    @property
    def avatar(self):
        '''统一的头像地址'''
        return self.plt_icon if self.plt_icon else self.icon.url

    def has_prem(self, prem):
        '''分级管理-权限检查'''
        need_prem = Permission.objects.get(name=prem)
        self_prem = Permission.objects.get(pk=self.prem_id)
        return  self_prem.level >=  need_prem.level


class Permission(models.Model):
    level = models.IntegerField()
    name = models.CharField(max_length=30, unique=True )

