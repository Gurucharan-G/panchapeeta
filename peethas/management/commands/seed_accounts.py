from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from peethas.models import Peetha, PeethaHandler


class Command(BaseCommand):
    help = 'Seeds admin and 5 Peetha handler accounts'

    def handle(self, *args, **options):
        self.stdout.write('Seeding user accounts...')

        # 1. Create Superuser (Admin)
        admin_username = 'admin'
        admin_pass = 'admin_password_123'
        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                email='admin@panchapeetha.org',
                password=admin_pass
            )
            self.stdout.write(self.style.SUCCESS(f'Created Superuser: "{admin_username}" / password: "{admin_pass}"'))
        else:
            self.stdout.write(f'Superuser "{admin_username}" already exists.')

        # 2. Create Handler Accounts
        handlers_info = [
            {
                'slug': 'rambhapuri',
                'username': 'rambhapuri_handler',
                'password': 'rambhapuri_pass_123',
                'email': 'rambhapuri@panchapeetha.org'
            },
            {
                'slug': 'ujjaini',
                'username': 'ujjaini_handler',
                'password': 'ujjaini_pass_123',
                'email': 'ujjaini@panchapeetha.org'
            },
            {
                'slug': 'kedara',
                'username': 'kedara_handler',
                'password': 'kedara_pass_123',
                'email': 'kedara@panchapeetha.org'
            },
            {
                'slug': 'srisaila',
                'username': 'srisaila_handler',
                'password': 'srisaila_pass_123',
                'email': 'srisaila@panchapeetha.org'
            },
            {
                'slug': 'kashi',
                'username': 'kashi_handler',
                'password': 'kashi_pass_123',
                'email': 'kashi@panchapeetha.org'
            },
        ]

        for info in handlers_info:
            try:
                peetha = Peetha.objects.get(slug=info['slug'])
            except Peetha.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Peetha with slug '{info['slug']}' not found in database. Please run seed_peethas first!"))
                continue

            # Check if user exists
            user, created = User.objects.get_or_create(
                username=info['username'],
                defaults={
                    'email': info['email']
                }
            )
            
            if created:
                user.set_password(info['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created User '{info['username']}' with password '{info['password']}'"))
            else:
                self.stdout.write(f"User '{info['username']}' already exists.")

            # Get or create PeethaHandler profile
            handler_profile, profile_created = PeethaHandler.objects.get_or_create(
                user=user,
                defaults={
                    'peetha': peetha
                }
            )

            if profile_created:
                self.stdout.write(self.style.SUCCESS(f"Associated '{info['username']}' as handler for '{peetha.name}'"))
            else:
                # Update existing handler profile to point to correct Peetha if needed
                if handler_profile.peetha != peetha:
                    handler_profile.peetha = peetha
                    handler_profile.save()
                    self.stdout.write(self.style.SUCCESS(f"Updated '{info['username']}' handler profile to '{peetha.name}'"))

        self.stdout.write(self.style.SUCCESS('User account seeding complete.'))
