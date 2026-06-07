from django.core.management.base import BaseCommand
from peethas.models import Peetha, Pooja

class Command(BaseCommand):
    help = 'Seeds sample poojas for Ujjaini Peetha'

    def handle(self, *args, **kwargs):
        try:
            peetha = Peetha.objects.get(slug='ujjaini')
        except Peetha.DoesNotExist:
            self.stdout.write(self.style.ERROR('Ujjaini Peetha not found. Run seed_peethas first.'))
            return

        poojas = [
            {
                'name': 'Sahasranama Archana',
                'description': 'Archana chanting the 1000 names of Lord Shiva for profound blessings.',
                'price': 501.00,
                'order': 1,
            },
            {
                'name': 'Eka Vara Rudrabhisheka',
                'description': 'Chanting of Sri Rudram one time with Abhisheka.',
                'price': 251.00,
                'order': 2,
            },
            {
                'name': 'Anna Dasoha (Annadana Seva)',
                'description': 'Contribution towards feeding devotees visiting the Peetha.',
                'price': 1000.00,
                'order': 3,
            },
            {
                'name': 'Vahana Pooja',
                'description': 'Special blessings for a newly purchased vehicle to ensure safety.',
                'price': 301.00,
                'order': 4,
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

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created_count} poojas for Ujjaini Peetha.'))
