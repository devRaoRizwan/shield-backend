from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_inquiry"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="products/"),
        ),
        migrations.AddField(
            model_name="product",
            name="image_content_type",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="product",
            name="image_data",
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="image_name",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
