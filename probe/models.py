from django.db import models
from django.urls.base import reverse_lazy

from publish.shell import differences


class Probe(models.Model):

    name = models.CharField(max_length=100)
    expected = models.TextField(default='Initial Output', null=True)
    source = models.TextField(default='none')
    passed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse_lazy('test_list')

    @staticmethod
    def create(**kwargs):
        x = Probe.objects.get_or_create(name=kwargs.get('name'))[0]
        expected = kwargs.get('expected')
        if expected:
            x.expected = expected
        x.source = kwargs.get('source')
        x.save()


class TestResult(models.Model):

    probe = models.ForeignKey(Probe, on_delete=models.CASCADE, editable=False)
    date = models.DateTimeField(auto_now=True)
    output = models.TextField(default='Not yet run')
    passed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.probe.name} - {self.date} - {self.passed}'

    def get_absolute_url(self):
        return reverse_lazy('test_list')

    @property
    def difference(self):
        return differences(self.output, self.probe.expected)

    @staticmethod
    def create(**kwargs):
        c = TestResult.objects.create(probe=kwargs.get('probe'))
        c.output = kwargs.get('output')
        c.passed = kwargs.get('passed')
        c.save()
        return c
