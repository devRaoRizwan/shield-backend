from django.core.management.base import BaseCommand

from catalog.models import Product


SAMPLE_PRODUCTS = [
    {
        "name": "Shield Tactical Backpack",
        "slug": "shield-tactical-backpack",
        "description": "A rugged backpack designed for everyday carry and field use.",
        "details": "Water-resistant build, reinforced zippers, multiple compartments, and padded support for extended use.",
        "customization_option": "Logo embroidery available on request",
        "sort_order": 1,
    },
    {
        "name": "Shield Utility Pouch",
        "slug": "shield-utility-pouch",
        "description": "A compact pouch for organizing tools, accessories, or small gear.",
        "details": "Durable stitched construction with secure fasteners and practical internal storage layout.",
        "customization_option": "Custom color accents available",
        "sort_order": 2,
    },
    {
        "name": "Shield Field Organizer",
        "slug": "shield-field-organizer",
        "description": "A lightweight organizer case for documents, devices, and essentials.",
        "details": "Slim profile, secure closure, and structured interior for keeping everyday items in place.",
        "customization_option": "Personalized label patch available",
        "sort_order": 3,
    },
]


class Command(BaseCommand):
    help = "Seed sample catalog products for local development."

    def handle(self, *args, **options):
        created_count = 0

        for product_data in SAMPLE_PRODUCTS:
            _, created = Product.objects.update_or_create(
                slug=product_data["slug"],
                defaults={
                    **product_data,
                    "is_active": True,
                },
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed complete. Created {created_count} new products and updated existing sample entries."
            )
        )
