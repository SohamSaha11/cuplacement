from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.hashers import make_password, check_password
from website.models import users, companies, notices, placedrecord, reviews

# Create your views here.

def index(request):
    return render(request, 'index.html')



def studentSignUp(request):
    error = "NULL"
    check = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        value = {
            'name' : name,
            'email': email
        }
        if not name or not email or not password:
            error = "All Fields Required. Please try again."
            check = True           
        elif '@thapar.edu' not in email:
            error = "Email must belong to thapar.edu, Please try again."
            check = True
        elif users.objects.filter(email=email).exists():
            error = "Email already exist. Please try again."
            check = True
        
        if check:
            data = {
                'error': error,
                'values': value
            }
            return render(request, 'studentSignUp.html', data)
        else:            
            user = users( name = name, email = email, password = make_password(password), isPlacementCell = False)
            user.save()
            # return render(request, 'studentSignUp.html', {'error': error})
            # a = users.objects.all()
            # a.delete()
            user = users.objects.get(email=email)
            request.session['userID'] = user.id
            return redirect('/home')
            # return HttpResponse(name + "<br>" + email + "<br>" + password)
    else:        
        return render(request, 'studentSignUp.html')



def studentLogIn(request):
    error = "Invalid login or password. Please try again."
    flag = False
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            flag = True
        elif users.objects.filter(email=email).exists() == False:
            flag = True
        else:
            user = users.objects.get(email=email)
            if check_password(password, user.password) == False :
                flag = True
            else:
                request.session['userID'] = user.id
                return redirect('/home')
        if flag:            
            return render(request, 'studentLogIn.html', {'error': error})

    else:
        id = request.session.get('userID')
        if id:
            return redirect("/home")
        return render(request, 'studentLogIn.html')



def home(request): 
    company = ""
    # girlsOnly = False
    if request.method == 'GET':
        offer = request.GET.get('o')
        year = request.GET.get('y')
        girlsOnly = request.GET.get('g')
        search = request.GET.get('q')
        if not offer:
            offer = "internship"
        if not year:
            year = 2021
        if not girlsOnly:
            girlsOnly = "False"

        id = request.session.get('userID')
        if not id:
            return redirect("/student/login")
        user = users.objects.get(id = id)
        if offer == "internship":
            if girlsOnly == "True":
                company = companies.objects.filter(girlsOnly = True)
            else:
                company = companies.objects.all()
            
        data = {
            'offer': offer,
            'year': year,
            'girlsOnly': girlsOnly,
            'user': user,
            'companies': company
        }
        return render(request, 'home.html', data)
    
    else:
        offer = request.POST.get('o')
        id = request.POST.get('compID')
        data = {
            'offer': offer,
            'compID': id
        }
        return viewCompany(request, data)



def logout(request):
    request.session.clear()
    return redirect("/")




def pcLogIn(request):
    error = "Invalid login or password. Please try again."
    flag = False
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            flag = True
        elif users.objects.filter(email=email).exists() == False:
            flag = True
        else:
            user = users.objects.get(email=email)
            if user.isPlacementCell == False:
                flag = True
            elif check_password(password, user.password) == False :
                flag = True
            else:
                request.session['userID'] = user.id
                return redirect('/home')
        if flag:            
            return render(request, 'pcLogIn.html', {'error': error})

    else:
        id = request.session.get('userID')
        if id:
            return redirect("/home")
        return render(request, 'pcLogIn.html')



def pcSignUp(request):
    error = "NULL"
    check = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        value = {
            'name' : name,
            'email': email
        }
        if not name or not email or not password:
            error = "All Fields Required. Please try again."
            check = True           
        elif '@thapar.edu' not in email:
            error = "Email must belong to thapar.edu, Please try again."
            check = True
        elif users.objects.filter(email=email).exists():
            error = "Email already exist. Please try again."
            check = True
        
        if check:
            data = {
                'error': error,
                'values': value
            }
            return render(request, 'pcSignUp.html', data)
        else:            
            user = users( name = name, email = email, password = make_password(password), isPlacementCell = True)
            user.save()
            user = users.objects.get(email=email)
            request.session['userID'] = user.id
            return redirect('/home')
            # return HttpResponse(name + "<br>" + email + "<br>" + password)
    else:        
        return render(request, 'pcSignUp.html')



def addCompany(request):
    if request.method=='POST':
        offerType = request.POST.get('o')
        name = request.POST.get('companyName')
        desc = request.POST.get('description')
        branch = request.POST.get('branchesEligible')
        cgpa = request.POST.get('cgpa')
        stipend = request.POST.get('stipendOffer')
        addBenefits = request.POST.get('additionalBenefits')
        regLink = request.POST.get('registerLink')
        deadline = request.POST.get('deadline')
        pubDate =  request.POST.get('publishDate')
        girlsOnly = request.POST.get('girlsOnly')

        if not girlsOnly:
            girlsOnly = False

        if offerType == "internship":
            company = companies(companyName=name, description=desc, branchesEligible=branch,
                                cgpa=cgpa, stipendOffer=stipend, additionalBenefits=addBenefits,
                                registerLink=regLink, deadline=deadline, publishDate=pubDate,
                                girlsOnly=girlsOnly )
            company.save()
            return redirect('/home')
        # else:
        #     company = placement_companies(companyName=name, description=desc, branchesEligible=branch,
        #                         cgpa=cgpa, stipendOffer=stipend, additionalBenefits=additionalBenefits,
        #                         registerLink=regLink, deadline=deadline, publishDate=pubDate )
        #     company.save()

    else:
        id = request.session.get('userID')
        if not id:
            return redirect("/placementCell/login")
        else:
            user = users.objects.get(id=id)
            if user.isPlacementCell==False:
                return HttpResponse('<h1>ERROR</h1>')
            else:
                data = {
                    'user': user,
                }
                return render(request, 'addCompany.html', data)



def noticeBoard(request):
    id = request.session.get('userID')
    if not id:
        return redirect("/student/login")
    else:
        user = users.objects.get(id=id)
        notice = notices.objects.all().order_by('-pubDate')
        data = {
            'user': user,
            'notices': notice
        }
        return render(request, 'noticeBoard.html', data)



def addNotice(request):
    if request.method=='POST':
        offerType = request.POST.get('o')
        name = request.POST.get('companyName')
        notice = request.POST.get('notice')
        expDate = request.POST.get('expiryDate')
        pubDate = request.POST.get('publishDate')

        if offerType == "internship":
            x = notices( compName = name, notice = notice, expiryDate = expDate, pubDate = pubDate)
            x.save()
            return redirect('/home/noticeBoard')

        # else:
        #     notice = noticeBoard(companyName=name, notice=notice, expiryDate=expDate, publishDate=pubDate)
        #     notice.save()

    else:
        id = request.session.get('userID')
        if not id:
            return redirect("/placementCell/login")
        else:
            user = users.objects.get(id=id)
            if user.isPlacementCell==False:
                return HttpResponse('<h1>ERROR</h1>')
            else:
                data = {
                    'user': user,
                }
                return render(request, 'addNotice.html', data)



def viewCompany(request, data):
    id = request.session.get('userID')
    if not id:
        return redirect("/student/login")
    else:
        user = users.objects.get(id=id)
        comp = companies.objects.get(id = data['compID'])
        review = reviews.objects.all()
        for r in review:
            u = users.objects.get(id = r.user_id)
            r.name = u.name
        data['company'] = comp
        data['user'] = user
        data['reviews'] = review
        return render(request, 'viewCompany.html', data)



def placedRecord(request):
    id = request.session.get('userID')
    if not id:
        return redirect("/student/login")
    else:
        user = users.objects.get(id=id)
        # comp = companies.objects.get(id = data['compID'])
        # data['company'] = comp
        records = placedrecord.objects.all()
        data = {
            'user': user,
            'records': records
        }
        return render(request, 'placedRecord.html', data)



def addStudent(request):
    if request.method=='POST':
        offerType = request.POST.get('o')
        roll = request.POST.get('rollNumber')
        name = request.POST.get('name')
        email = request.POST.get('email')
        compName = request.POST.get('companyName')
        year = request.POST.get('year')
        offer = request.POST.get('accept')

        if not offer:
            offer = False

        if offerType == "internship":
            x = placedrecord( rollNumber = roll, name = name, email = email, companyName = compName,
                             year = year, accept = offer)
            x.save()
            return redirect('/home/placedRecord')

        # else:
        #     notice = noticeBoard(companyName=name, notice=notice, expiryDate=expDate, publishDate=pubDate)
        #     notice.save()

    else:
        id = request.session.get('userID')
        if not id:
            return redirect("/placementCell/login")
        else:
            user = users.objects.get(id=id)
            if user.isPlacementCell==False:
                return HttpResponse('<h1>ERROR</h1>')
            else:
                data = {
                    'user': user,
                }
                return render(request, 'addStudent.html', data)