from django.db import models


class Page(models.Model):
    STYLE_TYPE_CHOICES = (
        (0, 'default'),
    )
    title = models.CharField(max_length=255, help_text="标题")
    content = models.TextField(help_text='正文')
    style_type = models.IntegerField(choices=STYLE_TYPE_CHOICES, default=0, help_text='样式类型')
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)