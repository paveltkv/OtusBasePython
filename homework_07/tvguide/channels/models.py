from django.db import models


class Channel(models.Model):
    name = models.CharField(max_length=64, unique=True)
    resolution = models.CharField(max_length=32)
    desc = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name} ({self.get_categories()})'

    def get_categories(self):
        categories_list = self.channelcategory_set.all()
        return ', '.join(map(str, categories_list))


class ChannelCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    channel = models.ManyToManyField(Channel)

    def __str__(self):
        return f'{self.name}'