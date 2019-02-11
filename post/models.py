from django.db import models

# Create your models here.
from user.models import User


class Post(models.Model):
    uid = models.IntegerField()
    title = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        ordering = ['-created']

    @property
    def auth(self):
        # db = choose_db(self.uid)  #需要分库的操作
        # auth = User.objects.using(db).get(pk=self.uid)
        #动态为post添加_auth属性，优化数据库操作，防止每次取auth下的属性都要访问数据库
        #属性级别的缓存
        if not hasattr(self, '_auth'):
            self._auth = User.objects.get(pk=self.uid)
        return self._auth





