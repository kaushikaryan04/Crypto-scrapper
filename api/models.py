
from django.db import models
import uuid

class Job(models.Model):
    STATUS_CHOICES = (
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed")
    )
    job_id = models.UUIDField(primary_key = True , default = uuid.uuid4 )
    status = models.CharField(max_length=20,choices = STATUS_CHOICES , default = "IN_PROGRESS")


class Coin(models.Model):
    job = models.ForeignKey(Job, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class CoinOutput(models.Model):
    coin = models.OneToOneField(Coin, related_name='output', on_delete=models.CASCADE)
    price = models.CharField(max_length = 20)
    price_change = models.CharField(max_length = 10)
    market_cap = models.CharField(max_length = 20)
    market_cap_rank = models.CharField(max_length = 20)
    volume = models.CharField(max_length = 20)
    volume_rank = models.CharField(max_length = 20)
    volume_change = models.CharField(max_length = 20)
    circulating_supply = models.CharField(max_length = 20)
    total_supply = models.CharField(max_length = 20)
    diluted_market_cap = models.CharField(max_length = 20)

class Contract(models.Model):
    output = models.ForeignKey(CoinOutput, related_name='contracts', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

class Link(models.Model):
    output = models.ForeignKey(CoinOutput, related_name='links', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    link = models.URLField()
