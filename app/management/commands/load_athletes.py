from django.core.management.base import BaseCommand
import json
from django.utils.timezone import timedelta

from app.models import Athlete, Result


class Command(BaseCommand):
    years = [2020, 2021, 2022, 2023, 2024, 2025]
    distances = [
        'ultra',
        'sky'
    ]
    help = 'Loads athletes and their results from a JSON file'

    def handle(self, *args, **options):
        for year in self.years:
            for distance in self.distances:
                distance_float = 14.0 if distance=='sky' else 78.0
                json_file = 'src/results/{first}{second}.json'.format(
                    first=str(year),
                    second=distance
                )
                try:
                    with open(json_file, 'r') as file:
                        data = json.load(file)

                    for item in data:
                        first_name = item['First name']
                        last_name = item['Family name']
                        gender = item['Gender']
                        nationality = item['Nationality']

                        # Check if athlete already exists (to avoid duplicates)
                        athlete, created = Athlete.objects.get_or_create(
                            first_name=first_name,
                            last_name=last_name,
                            gender=gender,
                            nationality=nationality,
                            defaults={'year_of_birth': 1990, 'phone_number': 'N/A'}  # Default values
                        )

                        # Parse time (assuming "HH:MM:SS" format)
                        if item['Time'] == '':
                            result_time = None
                            position = 0
                        else:
                            time_parts = item['Time'].split(':')

                            hours = int(time_parts[0])
                            minutes = int(time_parts[1])
                            seconds = int(time_parts[2])
                            position = item['Ranking']
                            result_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)

                        result, created = Result.objects.get_or_create(
                            athlete=athlete,
                            year=year,
                            distance=distance_float,
                            result_time=result_time,  # Only provide defaults for fields not in the lookup
                            position=position
                        )

                        if not created:
                            self.stdout.write(
                                self.style.WARNING(f"Result for {athlete.first_name} in 2023 already exists, skipping."))


                    self.stdout.write(self.style.SUCCESS('Successfully loaded athletes and results'))

                except FileNotFoundError:
                    self.stdout.write(self.style.ERROR(f'JSON file "{json_file}" not found'))
                except json.JSONDecodeError:
                    self.stdout.write(self.style.ERROR('Invalid JSON format in the file'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))