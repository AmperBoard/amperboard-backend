from random import randrange

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from amper.models import Report, Item


class Command(BaseCommand):
    def handle(self, *args, **options):
        query = Item.objects.all()

        base = datetime.today()
        num_days = 90

        date_list = [base - timedelta(days=x) for x in range(0, num_days)]

        for date in date_list:
            for x in range(10):
                date = datetime(year=date.year, month=date.month, day=date.day, hour=randrange(10, 23),
                                second=date.second, minute=date.minute)
                item = query[randrange(1, query.count())]

                Report.objects.create(
                    item=item,
                    duration=randrange(0, 60),
                    consumption=item.consumption,
                    start_time=date,
                )
