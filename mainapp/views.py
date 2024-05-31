from django.shortcuts import render
import pandas as pd
from django.shortcuts import redirect
import os


def home(request):
    projectRootPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(projectRootPath, 'Employees.xlsx')
    df = pd.read_excel(filePath)
    employees = df.to_dict(orient='records')
    row_count = len(df)
    context = {
        'employees':employees,
        'row_count':row_count
    }
    searchQuery = request.GET.get('search', '')
    ageQuery = request.GET.get('age', '')
    dobQuery = request.GET.get('dob', '')
    salaryQuery = request.GET.get('salary', '')
    departmentQuery = request.GET.get('department', '')

    if request.method == 'GET' and any([searchQuery, ageQuery, dobQuery, salaryQuery, departmentQuery]):
        df = filter_data(df, searchQuery, ageQuery, dobQuery, salaryQuery, departmentQuery)
        employees = df.to_dict(orient='records')
        context['employees'] = employees

    if request.method == 'GET':
        if 'total_average_salary' in request.GET:
                total_average_salary = df['Salary'].mean()
                context['total_average_salary'] = total_average_salary
                

    if request.method == 'POST':
        if 'submit_average_salary' in request.POST:
            department = request.POST.get('department')
            department_df = df[df['Department'] == department]

            if not department_df.empty:
                average_salary = department_df['Salary'].mean()

                context['department_average_salary'] = {
                    'department': department,
                    'average_salary': average_salary
                }

    
    return render(request,'mainapp/homepage.html',context)


def filter_data(df, searchQuery, ageQuery, dobQuery, salaryQuery, departmentQuery):
    df_res = df.copy()

    if searchQuery:
        df_res = df_res[df_res['FullName'].str.contains(searchQuery, case=False)]

    if ageQuery:
        df_res = df_res[df_res['Age'] == int(ageQuery)]

    if dobQuery:
        df_res = df_res[pd.to_datetime(df_res['DOB']) == pd.to_datetime(dobQuery)]

    if salaryQuery:
        df_res = df_res[df_res['Salary'] == int(salaryQuery)]

    if departmentQuery:
        df_res = df_res[df_res['Department'].str.contains(departmentQuery, case=False)]

    return df_res

def update_employee(request, employee_id):
    projectRootPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(projectRootPath, 'Employees.xlsx')
    df = pd.read_excel(filePath)
    employees = df.to_dict(orient='records')
    employee = next((emp for emp in employees if emp['id'] == int(employee_id)), None)
    index_to_update = df[df['id'] == employee_id].index

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        age = int(request.POST.get('age'))
        dob = request.POST.get('dob')
        salary = int(request.POST.get('salary'))
        department = request.POST.get('department')

        df.loc[index_to_update, ['FullName', 'Age', 'DOB', 'Salary', 'Department']] = [full_name, age, dob, salary, department]

        df.to_excel(filePath, index=False)

        return redirect('home')
    
    return render(request, 'mainapp/update_employee.html',{'employee':employee})

def delete_employee(request, employee_id):
    projectRootPath = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(projectRootPath, 'Employees.xlsx')
    df = pd.read_excel(filePath)
    index_to_delete = df[df['id'] == employee_id].index
    df.drop(index_to_delete, inplace=True)
    df.to_excel(filePath, index=False)
    employees = df.to_dict(orient='records')
    return render(request, 'mainapp/homepage.html',{'employees': employees})



