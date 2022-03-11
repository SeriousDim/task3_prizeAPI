from django.db import models

class Prize(models.Model):
    description = models.CharField(max_length=256)


class Participant(models.Model):
    name = models.CharField(max_length=256)


class Promo(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=2000)
    prizes = models.ManyToManyField(Prize, default=None, blank=None, null=True, related_name='promos')
    participants = models.ManyToManyField(Participant, default=None, blank=None, null=True, related_name='promos')


class Result(models.Model):
    promo_id = models.ForeignKey(Promo, on_delete=models.PROTECT, null=True, related_name='results')
    winner = models.ForeignKey(Participant, on_delete=models.PROTECT, null=True, related_name='as_winner')
    prize = models.ForeignKey(Prize, on_delete=models.PROTECT, null=True)

