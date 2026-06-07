from django.core.management.base import BaseCommand
from peethas.models import Peetha, Pooja

class Command(BaseCommand):
    help = 'Seeds sample poojas for Kashi Peetha'

    def handle(self, *args, **kwargs):
        try:
            peetha = Peetha.objects.get(slug='kashi')
        except Peetha.DoesNotExist:
            self.stdout.write(self.style.ERROR('Kashi Peetha not found. Run seed_peethas first.'))
            return

        poojas = [
            {
                'name': 'Vishwanath Abhisheka',
                'description': 'Special abhisheka for Lord Vishwanath.',
                'price': 1501.00,
                'order': 1,
            },
            {
                'name': 'Ganga Aarti Sankalpa',
                'description': 'Special sankalpa performed during the evening Ganga Aarti.',
                'price': 501.00,
                'order': 2,
            },
            {
                'name': 'Maha Rudrabhisheka',
                'description': 'Elaborate Rudrabhisheka performed at the holy Kshetra.',
                'price': 2501.00,
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

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created_count} poojas for Kashi Peetha.'))
