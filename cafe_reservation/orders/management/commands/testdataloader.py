import csv

from django.core.management.base import BaseCommand
from django.conf import settings

from api.models import Dish


DATA = {Dish: 'test_dishes.csv'}


class Command(BaseCommand):
    """Импорт тестовых данных для блюд из файла в бд."""
    help = 'Import data from file to DB'

    def import_data_from_csv_file(self):
        for model, csv_file in DATA.items():
            with open(
                    f'{settings.BASE_DIR}/data/{csv_file}',
                    'r',
                    encoding='utf-8',
            ) as file:
                reader = csv.DictReader(file)

                for data in reader:
                    model.objects.get_or_create(
                        name=data['name'],
                        price=data['price']
                    )

        self.stdout.write(self.style.SUCCESS('Successfully loaded data'))

    def handle(self, *args, **options):
        self.import_data_from_csv_file()
