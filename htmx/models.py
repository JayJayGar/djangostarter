from django.db import models

from django.utils import timezone


class Response(models.Model):
    test_time  = models.DateTimeField(default=timezone.now)
    button1    = models.CharField(max_length=10)
    latency1   = models.FloatField()
    button2    = models.CharField(max_length=10, null=True, blank=True)
    latency2   = models.FloatField(null=True, blank=True)
    button3    = models.CharField(max_length=10, null=True, blank=True)
    latency3   = models.FloatField(null=True, blank=True)

    def __str__(self):
        return (
            f"{self.test_time.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"B1={self.button1} ({self.latency1:.3f}s) "
            f"B2={self.button2} ({self.latency2:.3f}s) "
            f"B3={self.button3} ({self.latency3:.3f}s)"
        )
