import pandas as pd
from django.core.management.base import BaseCommand
from tcs.models import TCS, File  # Import your models

class Command(BaseCommand):
    help = 'Import data from Excel to the database'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='The path to the Excel file to import')

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        
        # Read the Excel file
        df = pd.read_excel(excel_file, engine='openpyxl')

        # Iterate over DataFrame and save to the database
        for index, row in df.iterrows():
            # Assuming columns in Excel match your model fields
            # Example for TCS model
            file_instance, created = File.objects.get_or_create(file_name=row['file_name'])
            TCS.objects.create(
                testcase_name=row['testcase_name'],
                testcase_result=row['testcase_result'],
                testcase_type=row['testcase_type'],
                testcase_description=row['testcase_description'],
                file_id=file_instance,
                testcase_group=row['testcase_group']
            )
            self.stdout.write(self.style.SUCCESS(f"Imported {row['testcase_name']}"))

        self.stdout.write(self.style.SUCCESS('Successfully imported data from Excel'))
