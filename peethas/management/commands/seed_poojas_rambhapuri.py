from django.core.management.base import BaseCommand
from peethas.models import Peetha, Pooja

class Command(BaseCommand):
    help = 'Seeds sample poojas for Rambhapuri Peetha'

    def handle(self, *args, **kwargs):
        try:
            peetha = Peetha.objects.get(slug='rambhapuri')
        except Peetha.DoesNotExist:
            self.stdout.write(self.style.ERROR('Rambhapuri Peetha not found. Run seed_peethas first.'))
            return

        poojas = [
            {
                'name': 'Maha Rudrabhisheka',
                'description': 'A sacred ritual involving the continuous pouring of water, milk, honey, and ghee over the Shiva Linga while chanting Sri Rudram.',
                'price': 1001.00,
                'order': 1,
            },
            {
                'name': 'Panchamrutha Abhisheka',
                'description': 'Bathing of the deity with five sacred elements: milk, curd, honey, sugar, and ghee.',
                'price': 501.00,
                'order': 2,
            },
            {
                'name': 'Bilvarchana (108 names)',
                'description': 'Archana performed using 108 sacred Bilva leaves.',
                'price': 251.00,
                'order': 3,
            },
            {
                'name': 'Maha Mangalarathi',
                'description': 'Daily offering of light and chanting of the devotee\'s sankalpa.',
                'price': 51.00,
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

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created_count} poojas for Rambhapuri Peetha.'))
