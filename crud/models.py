from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()

    @classmethod
    def get_objects_from_replica(cls):
        return cls.objects.using("read_replica").all()

    def save_to_master(self):
        self.save(using="default")
