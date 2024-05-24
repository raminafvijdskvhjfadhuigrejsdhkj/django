from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название услуги")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Изображение")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    def __str__(self):
        return self.title
