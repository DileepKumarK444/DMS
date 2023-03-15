from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PermissionModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "dms_permission"


class GroupModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "dms_group"


class GroupPermissionModel(models.Model):
    id = models.AutoField(primary_key=True)
    group_id = models.ForeignKey(
        GroupModel, default=0, on_delete=models.CASCADE, db_column='group_id')
    permission_id = models.ForeignKey(
        PermissionModel, default=0, on_delete=models.CASCADE, db_column='permission_id')

    class Meta:
        db_table = "dms_group_permission"


class RoleModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "dms_roles"


class UserRoleModel(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        User, default=0, on_delete=models.CASCADE)
    role_id = models.ForeignKey(
        RoleModel, default=0, on_delete=models.CASCADE, db_column='role_id')

    class Meta:
        db_table = "dms_user_roles"


class RoleGroupModel(models.Model):
    id = models.AutoField(primary_key=True)
    role_id = models.ForeignKey(
        RoleModel, default=0, on_delete=models.CASCADE, db_column='role_id')
    group_id = models.ForeignKey(
        GroupModel, default=0, on_delete=models.CASCADE, db_column='group_id')

    def __str__(self):
        return self.role_id + 'role group'

    class Meta:
        db_table = "dms_role_group"
