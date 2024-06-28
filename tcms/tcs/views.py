from django.shortcuts import render, redirect
from .models import File, TCS ,Project
import os
from django.conf import settings
import pandas as pd
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.db.models import Count,Q
from django.utils.encoding import smart_str
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, staff_required, guest_allowed
from django.shortcuts import get_object_or_404
import shutil
import pandas as pd
from django.utils.timezone import localtime

def test_update(request):
    if request.method == 'POST':
        testcase_id = request.POST.get('testcase_id')
        filename=request.POST.get('file_name')
        group=request.POST.get('testcase_group')
        testcase_result = request.POST.get('testcase_result')   
        try:
            testcase = TCS.objects.get(pk=testcase_id)
            testcase.testcase_result = testcase_result
            testcase.save()
            return redirect('testcase_display', group=group, filename=filename)
        except TCS.DoesNotExist:
            # Handle the error if the testcase does not exist
            pass
    
    return redirect('testcase_display', group=group, filename=filename)
 
@login_required
def index(request):
    projects = Project.objects.all()   
    unique_combinations = TCS.objects.values('file_name', 'testcase_group').distinct()                            
    test_case_stats = TCS.objects.values('testcase_group').annotate(
        total=Count('testcase_id'),
        successful=Count('testcase_id', filter=Q(testcase_result='Successful')),
        failed=Count('testcase_id', filter=Q(testcase_result='Failed')),
        ongoing=Count('testcase_id', filter=Q(testcase_result='Ongoing'))
    )

    # Pass the stats to the template
    context = {
        'test_case_stats': test_case_stats,
        'projects':projects,
        'unique_combinations':unique_combinations,
        'user': request.user
    }

    return render(request, 'tcs_temp/index.html', context)

@login_required
@admin_required
def newproject(request):
    projects = Project.objects.all()
    unique_combinations = TCS.objects.values('file_name', 'testcase_group').distinct()          
    file_counts = {}
    for combination in unique_combinations:
        group = combination['testcase_group']
        if group not in file_counts:
            file_counts[group] = set()
        file_counts[group].add(combination['file_name'])
    
    # Convert the sets to counts
    file_counts = {group: len(files) for group, files in file_counts.items()}
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        try:
            project = Project.objects.create(project_name=project_name)
            messages.success(request, f'Project "{project.project_name}" created successfully!')
        except Exception as e:
            messages.error(request, f'Failed to create project: {str(e)}')
        return redirect(request.path)  # Redirect back to the same view


    return render(request, 'tcs_temp/new_project.html',{'projects': projects,'unique_combinations':unique_combinations,'file_counts': file_counts})


def profile(request):
   
    return render(request, 'tcs_temp/users-profile.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('index')  # Change 'home' to your desired redirect URL after login
        else:
            return render(request, 'tcs_temp/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'tcs_temp/login.html', {'form': form})

def search_results(request):
    projects = Project.objects.all()   
    unique_combinations = TCS.objects.values('file_name', 'testcase_group').distinct() 
    query = request.GET.get('query')
    search_results = None
    
    if query:
        # Adjust the field names according to your model
        search_results = File.objects.filter(file_name__icontains=query)
    print(query)
    return render(request, 'tcs_temp/search_results.html',
     {'search_results': search_results, 
      'query': query,
      'projects':projects,
      'unique_combinations':unique_combinations
      })
    

def clear_uploads_directory():
    """
    Deletes all files in the Testcases directory.
    """
    uploads_directory = os.path.join(settings.MEDIA_ROOT, 'uploads')
    if os.path.exists(uploads_directory):
        for file_name in os.listdir(uploads_directory):
            file_path = os.path.join(uploads_directory, file_name)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Delete the file or link
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)  # Remove the directory
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

@login_required
@staff_required
def upload_file(request):
    projects = Project.objects.all()
    unique_combinations = TCS.objects.values('file_name', 'testcase_group').distinct()
    print(unique_combinations)
    if request.method == 'POST':
        status_file = request.FILES.get('status_file')
        testcase_file = request.FILES.get('testcase_file')
        testcase_group = request.POST.get('testcase_group')
        project_instance = Project.objects.get(project_name=testcase_group)
        
        if not status_file or not testcase_file:
            messages.error(request, 'Both files must be uploaded. Please select both files and try again.')
            return redirect('upload')

        try:
            with transaction.atomic():
                # Save status file to the 'uploads' directory
                status_file_path = save_uploaded_file(status_file, 'uploads')
                testcase_file_path = save_uploaded_file(testcase_file, testcase_group)
                # Create File instance
              
                status_file_instance = File(
                    file_name=testcase_file.name,
                    file_path=testcase_file_path,
                    project_name=project_instance
                )
                status_file_instance.save()

                # Process the status file and save data to the TCS model
                process_excel_file(status_file_path, status_file_instance,request)
                clear_uploads_directory()
                # Save testcase file to the 'Testcases' directory
                
                messages.success(request, 'Files uploaded successfully. Status file processed and Testcase file uploaded.')

        except ValueError as ve:
            # If a ValueError is raised in process_excel_file, handle it here
            os.remove(testcase_file_path)
            clear_uploads_directory()
            messages.error(request, f"Error: {ve}")
        except Exception as e:
            # If any other exception is raised, handle it here
            messages.error(request, f'An error occurred during file upload: {e}')

        return redirect('upload')

    return render(request, 'tcs_temp/upload_testcase.html',{'projects': projects,'unique_combinations':unique_combinations,'user': request.user})

def process_excel_file(file_path, file_instance,request):
    """
    Process the uploaded Excel file and save its contents to the TCS model.
    """
    if request.method == 'POST':
        # Get the selected value from the form
        testcase_group = request.POST.get('testcase_group')
    df = pd.read_excel(file_path)

    required_columns = ['testcase_name', 'testcase_result', 'testcase_type', 'testcase_description', 'testcase_group']
    if not all(column in df.columns for column in required_columns):
        raise ValueError('Invalid file structure. Please use the standard file for the status file.')
    for index, row in df.iterrows():
        TCS.objects.create(
            testcase_name=row['testcase_name'],
            testcase_result=row['testcase_result'],
            testcase_type=row['testcase_type'],
            testcase_description=row['testcase_description'],
            file_name=file_instance,  # Associate the file instance
            testcase_group=testcase_group
        )


def save_uploaded_file(uploaded_file, directory):
    
    # Ensure the target directory exists
    target_directory = os.path.join(settings.MEDIA_ROOT, directory)
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Save the file to the specified directory
    file_path = os.path.join(target_directory, uploaded_file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_path

@login_required
def testcase_display(request, group,filename):
    # Use the 'group' parameter to filter test cases
    projects = Project.objects.all()  
    unique_combinations = TCS.objects.values('file_name', 'testcase_group').distinct()                            

    if filename =="a":
        testcases2 = TCS.objects.filter(testcase_group=group)
        
    else:
       testcases2 = TCS.objects.filter(testcase_group=group,file_name=filename)
    summary = (
        testcases2
        .values('testcase_group', 'testcase_result')
        .annotate(count=Count('testcase_id'))
        .order_by('testcase_group', 'testcase_result')
    )

    # Prepare the context to pass to the template
    context = {
        'projects':projects,
        'testcases2': testcases2,
        'selected_group': group,
        'unique_combinations':unique_combinations,
        'filename':filename,
        'user': request.user
    }

    return render(request, 'tcs_temp/testcase_display.html', context)


def download_file(request, file_name, group):
    # Construct the full file path
    file_directory = os.path.join(settings.MEDIA_ROOT, group)
    
    # Construct the full file path
    file_path = os.path.join(file_directory, file_name)
    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            # Prepare the response
            response = HttpResponse(file.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename={smart_str(os.path.basename(file_path))}'
            return response
    
    # If the file does not exist, raise a 404 error
    raise Http404("File not found")

def delete_project(request,project_name):
    deleted, _ = TCS.objects.filter(testcase_group=project_name).delete()
    del_project, _ =Project.objects.filter(project_name=project_name).delete()
    uploads_directory = os.path.join(settings.MEDIA_ROOT, project_name)
    if os.path.isdir(uploads_directory):
         shutil.rmtree(uploads_directory)
    return redirect('newproject')
def delete_file(request,file_name):
    file_obj = get_object_or_404(File, file_name=file_name)
    file_path = file_obj.file_path
    print(file_path)
    if os.path.isfile(file_path):
        os.unlink(file_path) 
    del_file, _ =File.objects.filter(file_name=file_name).delete()
    return redirect('newproject')


def export_to_excel(request,filename,group):
    # Fetch data from the database using Django ORM
    
    data = TCS.objects.filter(testcase_group=group,file_name=filename) .values(
            'testcase_id', 'testcase_name', 'testcase_result','testcase_type','testcase_description','testcase_group', 'created_at', 'updated_at'  # Add your actual field names here
        )
    print(data)
    df = pd.DataFrame(list(data))

    # Step 3: Format datetime fields for Excel
    if 'created_at' in df.columns:
        df['created_at'] = df['created_at'].apply(lambda x: localtime(x).strftime('%Y-%m-%d %H:%M:%S') if x else '')
    if 'updated_at' in df.columns:
        df['updated_at'] = df['updated_at'].apply(lambda x: localtime(x).strftime('%Y-%m-%d %H:%M:%S') if x else '')

    # Step 4: Create a buffer to hold the Excel file in memory
    from io import BytesIO
    buffer = BytesIO()

    # Step 5: Write the DataFrame to the buffer as an Excel file
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    # Step 6: Set up the filename
    # Get the filename from the query parameters or default to 'database_export.xlsx'
    

    # Ensure the filename ends with '.xlsx'
    if not filename.endswith('.xlsx'):
        filename += '.xlsx'

    # Step 7: Set up the HTTP response to serve the file
    buffer.seek(0)  # Move to the beginning of the buffer
    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response