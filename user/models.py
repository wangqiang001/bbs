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
    prem_id = models.IntegerField(default=1)

    @property
    def avatar(self):
        '''统一的头像地址'''
        return self.plt_icon if self.plt_icon else self.icon.url

    def roles(self):
        '''当前用户用户的所有角色'''
        relations = UserRoleRelation.objects.filter(user_id=self.id).only('role_id')
        role_id_list = [role.role_id for role in relations]
        return  Role.objects.filter(id__in=role_id_list)

    def has_prem(self, prem):
        '''分级管理-权限检查-是否有权限'''
        need_prem = Permission.objects.get(name=prem)
        self_prem = Permission.objects.get(pk=self.prem_id)
        return  self_prem.level >=  need_prem.level

    def has_prem_func(self, perm):
        '''功能-管理-权限检查-是否有权限'''
        for role in self.roles():
            for prem in role.perms():
                if prem.name == perm:
                    return True
        return False


class Permission(models.Model):
    '''分级权限表'''
    level = models.IntegerField()
    name = models.CharField(max_length=30, unique=True )


class Role(models.Model):
    '''角色表 admin manager user'''
    name = models.CharField(max_length=16, unique=True)

    def perms(self):
        '''当前角色拥有的所有权限'''
        relations = RolePermissionFuncRelation.objects.filter(role_id=self.id).only('perm_id')
        perm_id_list = [perm.perm_id for perm in relations]
        return PermissionFunc.objects.filter(pk__in=perm_id_list)

class PermissionFunc(models.Model):
    '''功能权限表，add_post del_post add_comment del_comment'''
    name = models.CharField(max_length=16, unique=True)

class RolePermissionFuncRelation(models.Model):
    '''角色-功能权限-关系'''
    role_id = models.IntegerField()
    perm_id = models.IntegerField()

    @classmethod
    def add_perm_for_role(cls, role_id, perm_id):
        cls.objects.create(role_id=role_id, perm_id=perm_id)

    @classmethod
    def del_perm_from_role(cls, role_id, perm_id):
        cls.objects.get(role_id=role_id, perm_id=perm_id).delete()


class UserRoleRelation(models.Model):
    '''角色-用户-关系'''
    user_id = models.IntegerField()
    role_id = models.IntegerField()

    @classmethod
    def add_role_for_user(cls, user_id, role_id):
        cls.objects.create(user_id=user_id, role_id=role_id)

    @classmethod
    def del_role_from_user(cls, user_id, role_id):
        cls.objects.get(user_id=user_id, role_id=role_id).delete()


