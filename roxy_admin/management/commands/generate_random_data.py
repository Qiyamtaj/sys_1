from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from roxy_admin.models import User, Volunteer, Surfer
from faker import Faker
from random import choice, randint
from django.utils import timezone


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs['total']
        genders = ['Male', 'Female','Non-binary','Other']
        races = ['White', 'Coloured', 'African']
        roles = ['Volunteer', 'Surfer']

        for i in range(total):
            User.objects.create(email=fake.email(), 
                                first_name=fake.first_name(), 
                                last_name=fake.last_name(), 
                                password=get_random_string(10))
            
        for user in User.objects.filter(is_admin=False):
            role = choice(roles)
            if role == 'Volunteer':
                Volunteer.objects.create(
                    user=user,
                    phone_number=fake.phone_number(),
                    address=fake.address(),
                    country=fake.country(),
                    DOB=fake.date_of_birth(minimum_age=18, maximum_age=90),
                    gender=choice(genders),
                    race=choice(races),
                    hours=randint(1, 50),
                    attendance=randint(1, 50),
                    role=('Volunteer'),
                    medical_issues=fake.text(),
                    occupation=fake.job(),
                    offered_services=fake.text(),
                    availablity=fake.day_of_week(),
                    extra_info=fake.text(),
                    swim_longer_than_5_min=choice([True, False]),
                    comfortablity_in_ocean=fake.word(),
                    previous_volunteer=choice([True, False]),
                    age=randint(18, 90),
                    emergency_contact_first_name=fake.first_name(),
                    emergency_contact_last_name=fake.last_name(),
                    emergency_contact_cell=fake.phone_number(),
                    medical_aid=fake.word(),
                    medical_aid_num=fake.random_number(digits=8),
                    receive_newsletter=choice(['Yes', 'No']),
                    accept_TandC=choice(['Yes', 'No']),
                )
            elif role == 'Surfer':
                Surfer.objects.create(
                    user=user,
                    phone_number=fake.phone_number(),
                    address=fake.address(),
                    country=fake.country(),
                    DOB=fake.date_of_birth(minimum_age=18, maximum_age=90),
                    onset_of_condition=timezone.now() - timezone.timedelta(days=randint(1, 365)),
                    gender=choice(genders),
                    race=choice(races),
                    medical_issues=fake.text(),
                    occupation=fake.job(),
                    school=fake.word(),
                    diagnosis_and_needs=fake.text(),
                    hours=randint(1, 50),
                    attendance=randint(1, 50),
                    role=('Surfer'),
                    disability=fake.word(),
                    medication=fake.text(),
                    extra_info=fake.text(),
                    swim_longer_than_5_min=choice([True, False]),
                    comfortablity_in_ocean=fake.word(),
                    age=randint(18, 90),
                    emergency_contact_first_name=fake.first_name(),
                    emergency_contact_last_name=fake.last_name(),
                    emergency_contact_cell=fake.phone_number(),
                    medical_aid=fake.word(),
                    medical_aid_num=fake.random_number(digits=8),
                    receive_newsletter=choice(['Yes', 'No']),
                    accept_TandC=choice(['Yes', 'No']),
                )
            
            self.stdout.write(self.style.SUCCESS(f'Successfully generated {total} users.'))