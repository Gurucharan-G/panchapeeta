import os

peetha_titles = {
    'kashi': 'Kashi',
    'rambhapuri': 'Rambhapuri',
    'ujjaini': 'Ujjaini',
    'kedara': 'Kedara',
    'srisaila': 'Srisaila'
}

def fix_seed_file(peetha):
    filepath = rf"c:\Users\Bhoja\.gemini\antigravity-ide\scratch\panchapeetas\peethas\management\commands\seed_{peetha}.py"
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # If it doesn't have class Command, add it
    if "class Command(BaseCommand):" not in content:
        title = peetha_titles[peetha]
        command_class = f"""

class Command(BaseCommand):
    help = "Seeds/updates the database record for {title} Peetha"

    def handle(self, *args, **options):
        obj, created = Peetha.objects.update_or_create(
            slug=PEETHA_DATA["slug"],
            defaults=PEETHA_DATA,
        )
        status = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"  {{status}}: {{obj.name}}"))
"""
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(command_class)
        print(f"Fixed {filepath}")
    else:
        print(f"{filepath} is already fine.")

for p in peetha_titles.keys():
    fix_seed_file(p)
