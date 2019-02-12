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

    @property
    def comments(self):
        return Comment.objects.filter(post_id=self.id)

    @property
    def tags(self):
        relations = PostTagRrlation.objects.filter(post_id=self.id).only('tag_id')
        tag_id_list = [r.tag_id for r in relations]
        return Tag.objects.filter(id__in=tag_id_list)

    def update_tags(self, tag_names):
        '''更新帖子对应的和标签的关系表'''
        updated_tags = set(Tag.ensure_tags(tag_names))   #更新玩以后所有的tag，确保传入的标签已存在，不存在创建
        exist_tags = set(self.tags)           #当前已经有的tag

        #增加帖子的对应标签的关系表
        new_tags = updated_tags - exist_tags
        need_create_tid_list = [t.id for t in new_tags]    #需要建立关联的tag
        PostTagRrlation.add_relations(self.id, need_create_tid_list)

        # 删除帖子的对应标签的关系表
        old_tags = exist_tags - updated_tags
        need_del_tid_list = [t.id for t in old_tags]
        PostTagRrlation.del_relations(self.id, need_del_tid_list)


class Comment(models.Model):
    uid = models.IntegerField()
    post_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ['-created']

    @property
    def auth(self):
        if not hasattr(self, '_auth'):
            self._auth = User.objects.get(pk=self.uid)
        return self._auth

    @property
    def post(self):
        if not hasattr(self, '_auth'):
            self._post = Post.objects.get(pk=self.uid)
        return self._post


class Tag(models.Model):
    name = models.CharField(max_length=16, unique=True)

    @classmethod
    def ensure_tags(cls, tag_names):
        '''确保传入的tag已存在，如果不存在直接创建出来'''
        exist_tags = cls.objects.filter(name__in=tag_names)
        exist_names = [t.name for t in exist_tags]

        #创建不存在的tag
        not_exist_names = set(tag_names) - set(exist_names)
        need_create_tags = [Tag(name=name) for name in not_exist_names]
        cls.objects.bulk_create(need_create_tags)
        return cls.objects.filter(name__in=tag_names)

class PostTagRrlation(models.Model):
    '''帖子和标签的关系'''
    post_id = models.IntegerField()
    tag_id = models.IntegerField()

    @classmethod
    def add_relations(cls, post_id, tag_id_list):
        need_create = [cls(post_id=post_id, tag_id=tid) for tid in tag_id_list]
        cls.objects.bulk_create(need_create)

    @classmethod
    def del_relations(cls, post_id, tag_id_list):
        cls.objects.filter(post_id=post_id, tag_id__in=tag_id_list).delete()