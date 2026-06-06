from django.core.management.base import BaseCommand
from django.core.management import call_command
from peethas.models import Peetha

class Command(BaseCommand):
    help = "Seeds the database with all 5 Pancha Peethas by invoking their individual commands"

    def handle(self, *args, **options):
        self.stdout.write("Seeding all 5 Peethas by running individual commands...\n")
        
        call_command('seed_rambhapuri')
        call_command('seed_ujjaini')
        call_command('seed_kedara')
        call_command('seed_srisaila')
        call_command('seed_kashi')
        
        self.stdout.write(self.style.SUCCESS(f"\nDone! All {Peetha.objects.count()} Peethas are seeded in the database."))
