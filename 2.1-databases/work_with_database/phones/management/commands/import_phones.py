import csv
import re

from django.core.management.base import BaseCommand
from phones.models import Phone


def slug_construction(base_string):
    res1 = re.sub(' ', '-', base_string)
    res2 = re.findall(r'[-a-zA-Z0-9_]+', res1)
    return (''.join(res2)).lower()


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            new_phone = Phone(
                name=phone['name'],
                price=phone['price'],
                image=phone['image'],
                release_date=phone['release_date'],
                lte_exists=phone['lte_exists'],
                slug=slug_construction(phone['name']),
            )
            new_phone.save()
