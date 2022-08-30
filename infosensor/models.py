# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class InfoDados(models.Model):
    sensor = models.ForeignKey('InfoSensores', models.DO_NOTHING, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    capacitancia = models.FloatField(blank=True, null=True)
    umidade = models.FloatField(blank=True, null=True)
    precipitacao = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.sensor

    class Meta:
        managed = False
        db_table = 'info_dados'

    @property
    def popup_dados(self):
        popup = f"<span>Sensor: {self.sensor}<span>"
        popup += f"<span>Data: {self.data}<span>"
        popup += f"<span>Hora: {self.hora}<span>"
        popup += f"<span>Capacitancia: {self.capacitancia}<span>"
        popup += f"<span>Umidade: {self.umidade}<span>"

        return popup


class InfoSensores(models.Model):
    nome_sensor = models.CharField(primary_key=True, max_length=5)
    geom = models.PointField(srid=4326)
    funcao = models.CharField(max_length=20)
    cultura = models.CharField(max_length=50, blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    profundidade = models.FloatField(blank=True, null=True)
    cap_campo = models.FloatField(blank=True, null=True)
    murcha_pmt = models.FloatField(blank=True, null=True)
    adt = models.FloatField(blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome_sensor


    class Meta:
        managed = False
        db_table = 'info_sensores'

    @property
    def popup_content(self):
        popup = f"<span>Nome do Sensor: {self.nome_sensor}<span>"
        popup += f"<span>Coordenada: {self.geom}<span>"
        popup += f"<span>Altitude: {self.altitude}<span>"
        popup += f"<span>Profundidade: {self.profundidade}<span>"
        popup += f"<span>Cultura: {self.cultura}<span>"

        return popup


