import csv
import json

from django.core.management.base import BaseCommand
from books.models import Book


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            action='store',
            help='Выгрузить файл Json в базу данных'
        )

    def handle(self, *args, **options):
        with open(options['file_path'], 'r') as file:
            books = json.load(file)

        for book in books:
            new_book = Book(
                name=book['fields']['name'],
                author=book['fields']['author'],
                pub_date=book['fields']['pub_date'],
            )
            new_book.save()
