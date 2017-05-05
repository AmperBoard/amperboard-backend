from random import randrange

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from amper.models import Report, Item


class Command(BaseCommand):
    def handle(self, *args, **options):
        query = Item.objects.all()

        base = datetime.today()
        num_days = 90

        date_list_past = [base - timedelta(days=x) for x in range(0, num_days)]
        date_list_future = [base + timedelta(days=x) for x in range(0, num_days)]

        for date in date_list_past:
            for x in range(3):
                date = datetime(year=date.year, month=date.month, day=date.day, hour=randrange(10, 23),
                                second=date.second, minute=date.minute)
                item = query[randrange(1, query.count())]

                Report.objects.create(
                    item=item,
                    duration=randrange(0, 60),
                    consumption=250 - randrange(0, 500),
                    start_time=date,
                )

        for date in date_list_future:
            for x in range(3):
                date = datetime(year=date.year, month=date.month, day=date.day, hour=randrange(10, 23),
                                second=date.second, minute=date.minute)
                item = query[randrange(1, query.count())]

                Report.objects.create(
                    item=item,
                    duration=randrange(0, 60),
                    consumption=250 - randrange(0, 500),
                    start_time=date,
                )
