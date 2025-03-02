from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Employee, Notification
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


#employee login
def employee_login(request):
    if request.method == 'POST':
        empnumber = request.POST.get('empnumber')
        empmail = request.POST.get('empmail')

        # Check if the employee exists
        employee = Employee.objects.filter(empnumber=empnumber, empmail=empmail).first()
        if employee:
            request.session['employee_id'] = employee.id  # Store employee ID in session
            return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid Employee Number or Email.")
    return render(request, 'empapp/employee_login.html')

def employee_details(request):
    # Retrieve the employee ID from the session
    employee_id = request.session.get('employee_id')


    if not employee_id:
        messages.error(request, "You must log in first.")
        return redirect('employee_login')

    # Get the employee object
    employee = Employee.objects.filter(id=employee_id).first()
    print(employee)
    if not employee:
        messages.error(request, "Employee not found.")
        return redirect('employee_login')
    
     # Render the dashboard with employee details
    return render(request, 'empapp/user_dashboard.html', {'employee': employee})

def submit_request(request):
    # Handle form submission for change requests
    if request.method == 'POST':
        change_request = request.POST.get('change_request')
        employee_id = request.session.get('employee_id')

        if change_request and employee_id:
            employee = get_object_or_404(Employee, id=employee_id)
            Notification.objects.create(employee=employee, message=change_request)
            messages.success(request, "Your request has been submitted successfully.")
        else:
            messages.error(request, "Please provide a valid change request.")
    return redirect('user_dashboard')


#admin login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_superuser:  # Check if the user is an admin
                login(request, user)
                return redirect('index')  # Redirect to index.html
            
            
            else:
                messages.error(request, 'Access denied. Admins only.')
        
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'empapp/login.html')
        
@login_required
def index(request):
    sort_by = request.GET.get('sort_by', 'empnumber')  
    search_query = request.GET.get('search', '')  
    notifications = Notification.objects.all().order_by('-created_at')
    
    if search_query:
        employees = Employee.objects.filter(
            empnumber__icontains=search_query  
        ).order_by(sort_by)                 
    else:
        employees = Employee.objects.all().order_by(sort_by)  
    context = {
        'notifications' : notifications,
        'emp': employees,
        'sort_by': sort_by,
        'search_query': search_query,
    }
    return render(request, 'empapp/index.html', context)

@login_required
def dashboard_with_notifications(request):
    # Fetch notifications to display in the navbar
    notifications = Notification.objects.all().order_by('-created_at')
    #print(notifications)
    employees = Employee.objects.all()
    #print(employees)
    context = {
        'emp': employees,
        'notifications': notifications
    }
    return render(request, 'empapp/index.html', context)

@login_required
def clear_notifications(request):
    if request.method == 'POST':
        Notification.objects.all().delete()
        messages.success(request, "All notifications have been cleared.")
    return redirect('index')

def view_info(request, id):
    emp = Employee.objects.get(pk = id)
    return render(request, 'empapp/index.html',{'emp': emp})

def add_employee(request):
    if request.method =="POST":
        empnumber = request.POST['empnumber']
        empname = request.POST['empname']
        empmail = request.POST['empmail']
        empcity = request.POST['empcity']
        Employee.objects.create(
            empnumber = empnumber,
            empname = empname,
            empmail = empmail,
            empcity = empcity
        )
        messages.success(request, "Employee added successfully!")
        return redirect(reverse('index'))
    

def delete_employee(request, id):
    if request.method == "POST":
        emp = get_object_or_404(Employee, id=id)
        emp.delete() 
        messages.success(request, "Employee deleted successfully!")
    return redirect(reverse('index'))

def update_employee(request,id):
    emp = get_object_or_404(Employee, id=id)

    if request.method =="POST":
        emp.empname = request.POST['empname']
        emp.empmail = request.POST['empmail']
        emp.empcity = request.POST['empcity']
        emp.save()

        messages.success(request, "Employee updated successfully!")
        return redirect(reverse('index'))
    return render(request,'empapp/index.html',{
        'emp': Employee.objects.all(),
        'emp_to_update': emp
    })

def logout_view(request):
    # Determine if the logout is coming from an employee or admin
    is_employee = 'employee_id' in request.session
    logout(request)
    
    # Redirect based on the session type
    if is_employee:
        return redirect('employee_login')
    else:
        return redirect('login')

