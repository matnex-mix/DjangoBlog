# Create your models here.
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class OAuthUser(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='user',
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    openid = models.CharField(max_length=50)
    nikename = models.CharField(max_length=50, verbose_name='username')
    token = models.CharField(max_length=150, null=True, blank=True)
    picture = models.CharField(max_length=350, blank=True, null=True)
    type = models.CharField(blank=False, null=False, max_length=50)
    email = models.CharField(max_length=50, null=True, blank=True)
    matedata = models.TextField(null=True, blank=True)
    created_time = models.DateTimeField('created at', default=now)
    last_mod_time = models.DateTimeField('last modified', default=now)

    def __str__(self):
        return self.nikename

    class Meta:
        verbose_name = 'oauthuser'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']


class OAuthConfig(models.Model):
    TYPE = (
        ('weibo', 'Weibo'),
        ('google', 'Google'),
        ('github', 'Github'),
        ('facebook', 'Facebook'),
        ('qq', 'QQ'),
    )
    type = models.CharField('type', max_length=10, choices=TYPE, default='a')
    appkey = models.CharField(max_length=200, verbose_name='AppKey')
    appsecret = models.CharField(max_length=200, verbose_name='AppSecret')
    callback_url = models.CharField(
        max_length=200,
        verbose_name='callback url',
        blank=False,
        default='http://www.baidu.com')
    is_enable = models.BooleanField(
        'enabled', default=True, blank=False, null=False)
    created_time = models.DateTimeField('created at', default=now)
    last_mod_time = models.DateTimeField('last modified', default=now)

    def clean(self):
        if OAuthConfig.objects.filter(
                type=self.type).exclude(
            id=self.id).count():
            raise ValidationError(_(self.type + 'already exists'))

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'oauthconfig'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
