from django.core.management.base import BaseCommand
from peethas.models import Peetha, Pooja

class Command(BaseCommand):
    help = 'Seeds sample poojas for Srisaila Peetha'

    def handle(self, *args, **kwargs):
        try:
            peetha = Peetha.objects.get(slug='srisaila')
        except Peetha.DoesNotExist:
            self.stdout.write(self.style.ERROR('Srisaila Peetha not found. Run seed_peethas first.'))
            return

        poojas = [
            {
                'name': 'Mallikarjuna Swamy Abhishekam',
                'description': 'Sacred abhisheka dedicated to the presiding deity.',
                'price': 1001.00,
                'order': 1,
            },
            {
                'name': 'Kumkuma Archana',
                'description': 'Archana performed for Goddess Bhramaramba with sacred kumkum.',
                'price': 501.00,
                'order': 2,
            },
            {
                'name': 'Anna Dasoha (Annadana)',
                'description': 'Donation for the daily feeding of pilgrims.',
                'price': 1000.00,
                'order': 3,
            },
        ]

        created_count = 0
        for p_data in poojas:
            pooja, created = Pooja.objects.get_or_create(
                peetha=peetha,
                name=p_data['name'],
                defaults={
                    'description': p_data['description'],
                    'price': p_data['price'],
                    'order': p_data['order'],
                    'is_active': True
                }
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created_count} poojas for Srisaila Peetha.'))
