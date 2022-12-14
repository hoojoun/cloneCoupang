from django_seed import Seed
from django.core.management.base import BaseCommand
from shops.models import *
from account.models import *
import random
class Command(BaseCommand):

    help = 'This command creates review'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', default=1, type=int, help="How many users do you want to create?"
        )

    def handle(self, *args, **options):
        number = options.get('number')
        seeder = Seed.seeder()
        seeder.add_entity(PurchaseHistory, number, {
            'user' : CustomUser.objects.order_by("?").first(),
            'product': Products.objects.order_by("?").first(),
            'Delivery': False,
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f'{number} users created!'))
