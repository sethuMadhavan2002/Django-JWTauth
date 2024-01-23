from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import pysolr


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()

    @classmethod
    def get_objects_from_replica(cls):
        return cls.objects.using("read_replica").all()

    def save_to_master(self):
        self.save(using="default")


class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title


@receiver(post_save, sender=Document)
def index_document(sender, instance, **kwargs):
    solr = pysolr.Solr(settings.SOLR_SERVER, always_commit=True)

    document_data = {
        "id": str(instance.id),
        "title": instance.title,
        "content": instance.content,
    }

    solr.add(document_data)


post_save.connect(index_document, sender=Document)
