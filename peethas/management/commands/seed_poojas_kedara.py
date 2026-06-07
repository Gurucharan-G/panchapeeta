from django.core.management.base import BaseCommand
from peethas.models import Peetha, Pooja

class Command(BaseCommand):
    help = 'Seeds sample poojas for Kedara Peetha'

    def handle(self, *args, **kwargs):
        try:
            peetha = Peetha.objects.get(slug='kedara')
        except Peetha.DoesNotExist:
            self.stdout.write(self.style.ERROR('Kedara Peetha not found. Run seed_peethas first.'))
            return

        poojas = [
            {
                'name': 'Kedaralingeshwara Abhisheka',
                'description': 'Special abhisheka to the presiding deity of Kedara Peetha.',
                'price': 1001.00,
                'order': 1,
            },
            {
                'name': 'Shanti Homa',
                'description': 'Fire ritual to appease navagrahas and bring harmony.',
                'price': 2501.00,
                'order': 2,
            },
            {
                'name': 'Bilva Archana',
                'description': 'Offering of sacred Bilva leaves.',
                'price': 101.00,
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

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created_count} poojas for Kedara Peetha.'))
