from dateutil.relativedelta import relativedelta
from datetime import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect
from openpyxl import Workbook
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError, transaction
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils import timezone


# Homepage
def homepage(request):
    return render(request, 'homepage.html')


# User + Surfer Create Form
def UserCreate_Surfer(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        surfer_form = SurferForm(request.POST)

        if user_form.is_valid() and surfer_form.is_valid():
            try:
                with transaction.atomic():  # ensures this is an atomic operation
                    user = user_form.save()

                    surfer_form = surfer_form.save(commit=False)
                    surfer_form.user = user
                    surfer_form.first_name = user.first_name  # Set fields before saving
                    surfer_form.last_name = user.last_name

                    surfer_form.save()
                return redirect('roxy:LoginRequest')

            except IntegrityError:  # exception for database errors
                user_form.add_error(None, 'There was a problem saving your details. Please try again.')
                # add any other exception types here as needed
            except Exception as e:  # general exception
                user_form.add_error(None, 'An unknown error occurred. Please try again.')
                # it would also be a good idea to log this error for your records
                print(str(e))
       
    else:
        user_form = UserCreationForm()
        surfer_form = SurferForm({'role':'Surfer'})

    return render(request, 'surferpages/become-a-surfer.html', {
        'user_form': user_form,
        'surfer_form': surfer_form
    })




# User + Volunteer Create Form
def UserCreate_Volunteer(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        volunteer_form = VolunteerForm(request.POST)

        if user_form.is_valid() and volunteer_form.is_valid():
            try:
                with transaction.atomic():  # ensures this is an atomic operation
                    user = user_form.save()

                    volunteer_form = volunteer_form.save(commit=False)
                    volunteer_form.user = user
                    volunteer_form.first_name = user.first_name  # Set fields before saving
                    volunteer_form.last_name = user.last_name

                    volunteer_form.save()
                return redirect('roxy:LoginRequest')

            except IntegrityError:  # exception for database errors
                user_form.add_error(None, 'There was a problem saving your details. Please try again.')
                # add any other exception types here as needed
            except Exception as e:  # general exception
                user_form.add_error(None, 'An unknown error occurred. Please try again.')
                # it would also be a good idea to log this error for your records
                print(str(e))
       
    else:
        user_form = UserCreationForm()
        volunteer_form = VolunteerForm({'role':'Volunteer'})

    return render(request, 'volunteerpages/become-a-volunteer.html', {
        'user_form': user_form,
        'volunteer_form': volunteer_form
    })


# Login function
def LoginRequest(request):
        context = {
            "Loginform": LoginForm()
        }
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     messages.success(request, 'logged in')
        #     if request.user.role == 'Volunteer':
        #         return redirect('roxy:VolunteerPage')
        #     if request.user.role == 'Surfer':
        #         return redirect('roxy:SurferPage')
        if user is not None and user.is_authenticated and user.is_admin:
            login(request, user)
            return redirect('roxy:AdminPage')
        else:
            messages.error(request, 'Login incorrect')
            return render(request, "login.html", context)


# Logout view
@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("homepage")

# Surfer page view
@login_required
def SurferPage(request):
    return render(request, "surferpages/surferpage.html",)

# Volunteer page view
@login_required
def VolunteerPage(request):
    return render(request,"volunteerpages/volunteerpage.html")

@login_required
def AdminPage(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("You don't have permission to access this page.")

    # Get the search query from the request
    query = request.GET.get('q')

    # Filter the surfers and volunteers based on the search query
    if query:
        search = query.replace(" ", "")
        surfers = Surfer.objects.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__email__icontains=search)
        )
        volunteers = Volunteer.objects.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__email__icontains=search)
        )
    else:
        surfers = Surfer.objects.all()
        volunteers = Volunteer.objects.all()

    users = User.objects.all()

    # Modify the query variable to display blank if it's None
    query = query if query else ""

    context = {
        "users": users,
        "surfers": surfers,
        "volunteers": volunteers,
        "query": query
    }
    return render(request, "adminpages/admin-home.html", context)




# Surfer details 
@login_required
def SurferDetails(request, pk):
    surfer = Surfer.objects.get(id=pk)
    context = {
        'surfer': surfer,
    }
    return render(request, 'adminpages/surfer-details.html', context)

# Volunteer details
@login_required
def VolunteerDetails(request, pk):
    volunteer = Volunteer.objects.get(id=pk)
    context = {
        'volunteer': volunteer,
    }
    return render(request, 'adminpages/volunteer-details.html', context)



# Surfer Edit
@login_required
def SurferEdit(request, pk):
    surfer = Surfer.objects.get(id=pk)

    user_form = UserChangeForm(instance=surfer.user)
    surfer_form = SurferForm(instance=surfer)

    context = {
        "user_form": user_form,
        "surfer_form": surfer_form,
        }

    if request.method == "POST":
        user_form = UserChangeForm(request.POST, instance=surfer.user)
        surfer_form = SurferForm(request.POST, instance=surfer)


        if user_form.is_valid() and surfer_form.is_valid():
            user_form.save()
            surfer_form.save()
        
            # this will direct to the volunteer/surfer detail view
            return redirect(reverse('roxy:SurferDetails', args=[surfer.pk]))
        
    return render(request, 'adminpages/surfer-edit.html', context)


                                                              
# Volunteer Edit
@login_required
def VolunteerEdit(request, pk):
    volunteer = Volunteer.objects.get(id=pk)
   

    user_form = UserChangeForm(instance=volunteer.user)
    volunteer_form = VolunteerForm(instance=volunteer)

    context = {
        "user_form": user_form,
        "volunteer_form": volunteer_form,
        }

    if request.method == "POST":
        user_form = UserChangeForm(request.POST, instance=volunteer)
        volunteer_form = VolunteerForm(request.POST, instance=volunteer)


        if user_form.is_valid() and volunteer_form.is_valid():


            user_form.save()
            volunteer_form.save()
            
            # this will direct to the volunteer/surfer detail view
            return redirect(reverse('roxy:VolunteerDetails', args=[volunteer.pk]))
        
    return render(request, 'adminpages/volunteer-edit.html', context)



#calendar_view
def calendar_view(request):
    events = Event.objects.all()
    return render(request, 'adminpages/calendar.html', {'events': events})

#add_event
def add_event(request): 
    context = {
        'add_event_form' : EventForm()
        }
    
    if request.method == 'POST':
        add_event_form = EventForm(request.POST)
        if add_event_form.is_valid():
            add_event_form.save()
            return redirect('roxy:Calendar')

    return render(request, 'adminpages/add-event.html', context)


def advanced_search(request):
    # Retrieve query parameters from the request
    if request.method == 'POST':
        selected_users = request.POST.getlist('selected_users')

        # Add the selected users to the session
        if 'selected_users' in request.session:
            # Here, we are converting session data into set to avoid duplicate entries and then back to list
            request.session['selected_users'] = list(set(request.session['selected_users']).union(selected_users))
        else:
            request.session['selected_users'] = selected_users

        request.session.modified = True  # Ensure the session is saved

        # Add the selected users to the session
        if 'selected_users' in request.session:
            request.session['selected_users'].extend(selected_users)
        else:
            request.session['selected_users'] = selected_users

        request.session.modified = True  # Ensure the session is saved
    
    param_names = [
        'q', 'race', 'gender', 'age_min', 'age_max', 'occupation', 'hours_min', 'hours_max', 'attendance',
        'disability', 'role'
    ]

    params = {name: request.GET.get(name, '') for name in param_names}

    # Apply the filters based on the query parameters
    # Initialize volunteers and surfers with all entries
    volunteers = Volunteer.objects.all()
    surfers = Surfer.objects.all()

    if params['q']:
        query = params['q'].replace(" ", "")
        volunteers = volunteers.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
        surfers = surfers.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))

    if params['race']:
        volunteers = volunteers.filter(race__icontains=params['race'])
        surfers = surfers.filter(race__icontains=params['race'])

    if params['gender']:
        volunteers = volunteers.filter(gender__iexact=params['gender'])
        surfers = surfers.filter(gender__iexact=params['gender'])

    if params['age_min'] and params['age_max']:
        min_dob = date.today() - relativedelta(years=int(params['age_max']))
        max_dob = date.today() - relativedelta(years=int(params['age_min']))

        volunteers = volunteers.filter(DOB__gte=min_dob, DOB__lte=max_dob)
        surfers = surfers.filter(DOB__gte=min_dob, DOB__lte=max_dob)


    if params['occupation']:
        volunteers = volunteers.filter(occupation__icontains=params['occupation'])
        surfers = surfers.filter(occupation__icontains=params['occupation'])

    if params['hours_min'] and params['hours_max']:
        volunteers = volunteers.filter(hours__gte=int(params['hours_min']), hours__lte=int(params['hours_max']))

    if params['attendance']:
        volunteers = volunteers.filter(attendance=int(params['attendance']))

    if params['disability']:
        surfers = surfers.filter(disability__icontains=params['disability'])

    if params['role']:
        volunteers = volunteers.filter(role__icontains=params['role'])
        surfers = surfers.filter(role__icontains=params['role'])

    context = {
        **params,
        'volunteers': volunteers,
        'surfers': surfers,
    }

    return render(request, 'adminpages/advanced_search.html', context)

# Export to Excel
def export_excel(request):
    
    if request.method == 'POST':
         selected_users_ids = request.session.get('selected_users', [])

    print(f'Selected users:{selected_users_ids}')

    # filter out any empty strings
    selected_users_ids = [id for id in selected_users_ids if id]

    # Select only the users whose IDs were passed in the POST request
    volunteers = Volunteer.objects.none() # define an empty QuerySet as default
    surfers = Surfer.objects.none() # define an empty QuerySet as default

    # create a workbook
    wb = Workbook()
    ws = wb.active

    # write the header
    ws.append(['First Name', 'Last Name', 'Gender', 'Age', 'Occupation', 'Disability', 'Role', 'Attendance', 'Hours'])

    # get volunteers and surfers by selected user ids
    volunteers = Volunteer.objects.filter(id__in=selected_users_ids)
    surfers = Surfer.objects.filter(id__in=selected_users_ids)



    # write volunteer rows
    for volunteer in volunteers:
        ws.append([
            volunteer.user.first_name,
            volunteer.user.last_name,
            volunteer.gender,
            volunteer.age,
            volunteer.occupation,
            '-',  # not sure about the disability field
            volunteer.role,
            volunteer.attendance,
            volunteer.hours,
        ])

    # write surfer rows
    for surfer in surfers:
        ws.append([
            surfer.user.first_name,
            surfer.user.last_name,
            surfer.gender,
            surfer.age,
            surfer.occupation,
            surfer.disability,
            surfer.role,
            surfer.attendance,
            surfer.hours,
        ])

    # Create response with excel data
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=selected_users.xlsx'
    wb.save(response)

      # Clear the selected users from the session after exporting
    if 'selected_users' in request.session:
        del request.session['selected_users']

    return response
 
# Storing selected users in session
def store_selected_users(request):
    if request.method == 'POST':
        selected_users = request.POST.getlist('selected_users')

        # Add the selected users to the session
        if 'selected_users' in request.session:
            request.session['selected_users'].extend(selected_users)
        else:
            request.session['selected_users'] = selected_users

        request.session.modified = True  # Ensure the session is saved

    return HttpResponse(status=204)  # return a 'no content' response

def QRScannerView(request):
    action_url = reverse('roxy:StartEndTracking')
    return render(request, 'adminpages/qr_scanner.html', {'action_url': action_url})


@csrf_exempt
def StartEndTracking(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    
    if 'action' not in body_data or 'id' not in body_data:
        return JsonResponse({'status': 'error', 'message': 'Missing required parameters'})

    action = body_data['action']
    qr_code_data = body_data['id']


    surfer = Surfer.objects.filter(id=qr_code_data).first()
    volunteer = Volunteer.objects.filter(id=qr_code_data).first()

    if surfer:
        return handle_time_tracking(request, surfer, action)
        
    elif volunteer:
        return handle_time_tracking(request, volunteer, action)
    
    else:
        return JsonResponse({'status': 'error', 'message': 'No surfer or volunteer found with the provided ID'}) 

def handle_time_tracking(request, user, action):
    if action == 'stop':
        if user.is_timing_active and user.start_time:
            end_time = timezone.now()
            elapsed_time = (end_time - user.start_time).total_seconds() / 3600
            user.hours += round(elapsed_time, 2)
            print(f"Users updated hours: {user.hours}")
            user.attendance += 1
            user.is_timing_active = False
            user.start_time = None  # Clear the start_time
            user.save()

            return JsonResponse({'status': 'ok', 'message': 'Time tracking ended. Hours updated.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No active tracking found for the user.'})
    
    elif action == 'start':   
        user.is_timing_active = True
        user.start_time = datetime.now()
        print(f"Users unupdated hours: {user.hours}")
        user.save()
        return JsonResponse({'status': 'ok', 'message': 'Time tracking started for the user.'})

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid action provided.'})
        

@csrf_exempt
def EndAllTracking(request):
    print("end all tracking called")

    # Authenticate the request to ensure that it's from an authorized source
    if not request.user.is_admin:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    # Find all active Surfer sessions and stop them
    active_surfers = Surfer.objects.filter(is_timing_active=True)
    active_surfer_count = active_surfers.count()  # Count before stopping the sessions

    for surfer in active_surfers:
        print(f"Active surfer: {surfer}")
        handle_time_tracking(request, surfer, 'stop')
        surfer.refresh_from_db()
        print(f"Is surfer {surfer} active = {surfer.is_timing_active}")

    # Find all active Volunteer sessions and stop them
    active_volunteers = Volunteer.objects.filter(is_timing_active=True)
    active_volunteer_count = active_volunteers.count()  # Count before stopping the sessions

    for volunteer in active_volunteers:
        print(f"Active volunteer: {volunteer}")
        handle_time_tracking(request, volunteer, 'stop')
        volunteer.refresh_from_db()
        print(f"Is volunteer {volunteer} active = {volunteer.is_timing_active}")

    # Combine both counts
    total_stopped_count = active_surfer_count + active_volunteer_count

    return JsonResponse({'status': 'ok', 'stopped_count': total_stopped_count})


@csrf_exempt
def SearchUsersByName(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    print(f"Body data: {body_data}") # Debug statement

    query = body_data.get('name', "")
    first_name, last_name = query.split(' ', 1) if ' ' in query else (query, "")

    # Querying both surfers and volunteers with the given name or email
    surfers = Surfer.objects.filter(Q(user__first_name__icontains=first_name, user__last_name__icontains=last_name) | Q(user__email__icontains=query))
    volunteers = Volunteer.objects.filter(Q(user__first_name__icontains=first_name, user__last_name__icontains=last_name) | Q(user__email__icontains=query))

    # Combine the results and serialize to JSON
    users = [{"first_name": user.user.first_name, "last_name": user.user.last_name, "id": user.id} for user in surfers] + \
            [{"first_name": user.user.first_name, "last_name": user.user.last_name, "id": user.id} for user in volunteers]

    return JsonResponse({'status': 'ok', 'users': users})

def GetUsername(request):
    user_id = request.GET.get('id')
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'User ID not provided.'}, status=400)

    user_object = None
    
    try:
        user_object = Volunteer.objects.get(id=user_id).user
        return JsonResponse({
            'status': 'ok',
            "first_name": user_object.first_name,
            "last_name": user_object.last_name
        })
    except Volunteer.DoesNotExist:
        pass

    if not user_object:
        try:
            user_object = Surfer.objects.get(id=user_id).user
            return JsonResponse({
            'status': 'ok',
            "first_name": user_object.first_name,
            "last_name": user_object.last_name
            })
        except Surfer.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)

    return JsonResponse({'status': 'ok', 'first_name': user_object.first_name, 'last_name': user_object.last_name})


# def generate_stats(request):
#     wb = Workbook()endallsessions
#         'ID',
#         'Phone Number',
#         'Address',
#         'Country',
#         'Date of Birth',
#         'Age',
#         'Onset of Condition',
#         'Gender',
#         'Race',
#         'Medical Issues',
#         'Occupation',
#         'School',
#         'Diagnosis and Needs',
#         'Hours',
#         'Attendance',
#         'Role',
#         'Disability',
#         'Medication',
#         'Extra Info',
#         'Can Swim Longer than 5 mins?',
#         'Comfortability in Ocean',
#         'Emergency Contact First Name',
#         'Emergency Contact Last Name',
#         'Emergency Contact Cell Number',
#         'Medical Aid',
#         'Medical Aid Number',
#         'Receive Newsletter',
#         'Accepted T&C'
#     ]

#     # write the header
#     surfer_page.append(header)

#     surfers = Surfer.objects.all()
    
#     for surfer in surfers:
#     ws.append([
#         surfer.user.username,  # Assuming the User model has a 'username' field
#         surfer.user.email,  # Assuming the User model has an 'email' field
#         surfer.id,
#         surfer.phone_number,
#         surfer.address,
#         surfer.country,
#         surfer.DOB,
#         surfer.age,
#         surfer.onset_of_condition,
#         surfer.gender,
#         surfer.race,
#         surfer.medical_issues,
#         surfer.occupation,
#         surfer.school,
#         surfer.diagnosis_and_needs,
#         surfer.hours,
#         surfer.attendance,
#         surfer.role,
#         surfer.disability,
#         surfer.medication,
#         surfer.extra_info,
#         surfer.swim_longer_than_5_min,
#         surfer.comfortablity_in_ocean,
#         surfer.emergency_contact_first_name,
#         surfer.emergency_contact_last_name,
#         surfer.emergency_contact_cell,
#         surfer.medical_aid,
#         surfer.medical_aid_num,
#         surfer.receive_newsletter,
#         surfer.accept_TandC
#     ])

#      # Create response with excel data
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename=yearly_stats.xlsx'
#     wb.save(response)

#     return response