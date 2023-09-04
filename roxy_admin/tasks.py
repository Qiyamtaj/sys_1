from datetime import datetime

from celery import shared_task
from .models import Volunteer, Surfer, VolunteerArchive, SurferArchive

@shared_task
def archive_and_reset_data():

    current_year = datetime.now().year

    # Getting volunteers and surfers whose financial_year is not the current year
    volunteers_to_archive = Volunteer.objects.exclude(financial_year=current_year)
    surfers_to_archive = Surfer.objects.exclude(financial_year=current_year)

    # Archive volunteers and surfers whose financial year is not current
    for volunteer in volunteers_to_archive:
        VolunteerArchive.objects.create(

            user=volunteer.user,
            financial_year=volunteer.financial_year,  # Note: We're archiving the old financial year, not the current
            phone_number=volunteer.phone_number,
            address = volunteer.address,
            country = volunteer.country,
            DOB = volunteer.DOB,
            age = volunteer.age,
            gender = volunteer.gender,
            race = volunteer.race,
            hours = volunteer.hours,
            attendance = volunteer.attendance,
            role = volunteer.role,
            medical_issues = volunteer.medical_issues,
            occupation = volunteer.occupation,
            offered_services = volunteer.offered_services,
            availablity = volunteer.availablity,
            extra_info = volunteer.extra_info,
            swim_longer_than_5_min = volunteer.swim_longer_than_5_min,
            comfortablity_in_ocean = volunteer.comfortablity_in_ocean,
            previous_volunteer = volunteer.previous_volunteer,
            emergency_contact_first_name = volunteer.emergency_contact_first_name,
            emergency_contact_last_name = volunteer.emergency_contact_last_name,
            emergency_contact_cell = volunteer.emergency_contact_cell,
            medical_aid = volunteer.medical_aid,
            medical_aid_num = volunteer.medical_aid_num,
            accept_TandC = volunteer.accept_TandC,
            qr_code = volunteer.qr_code
        )
    
    for surfer in surfers_to_archive:

        SurferArchive.objects.create(

            user = surfer.user ,
            financial_year = surfer.financial_year ,
            id = surfer.id ,
            phone_number = surfer.phone_number ,
            address = surfer.address ,
            country = surfer.country ,
            DOB = surfer.DOB ,
            age = surfer.age ,
            onset_of_condition = surfer.onset_of_condition ,
            gender = surfer.gender ,
            race = surfer.race ,
            medical_issues = surfer.medical_issues,
            occupation = surfer.occupation ,
            school = surfer.school ,
            diagnosis_and_needs =surfer.diagnosis_and_needs ,
            hours = surfer.hours ,
            attendance = surfer.attendance ,
            role = surfer.role ,
            disability = surfer.disability ,
            medication = surfer.medication ,
            extra_info = surfer.extra_info ,
            swim_longer_than_5_min = surfer.swim_longer_than_5_min ,
            comfortablity_in_ocean = surfer.comfortablity_in_ocean ,
            emergency_contact_first_name = surfer.emergency_contact_first_name ,
            emergency_contact_last_name = surfer.emergency_contact_last_name ,
            emergency_contact_cell = surfer.emergency_contact_cell ,
            medical_aid = surfer.medical_aid ,
            medical_aid_num = surfer.medical_aid_num ,
            accept_TandC = surfer.accept_TandC ,
            qr_code = surfer.qr_code ,
            
            )
    # You can add similar logic for surfers if you want to archive them too

    try:
        # Reset hours and attendance for Volunteer and Surfer models
        Volunteer.objects.all().update(financial_year=current_year, hours=0.0, attendance=0)
        Surfer.objects.all().update(financial_year=current_year, hours=0.0, attendance=0)

    except Exception as e:
        # Log the error for diagnosis
        print(f"Error occurred: {e}")


