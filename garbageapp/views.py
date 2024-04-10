from django.shortcuts import redirect, render
from django.contrib import messages
from garbageapp.models import driver, drivstatus, regcomp, userreg,bin

# Create your views here.
def index(request):
    if 'email' in request.session:
        current_user=request.session['email']
        user=userreg.objects.get(email=current_user)
        return render(request,"index.html",{'current_user':current_user,'user':user})
    return render(request,"index.html")
def userregister(request):
    if request.method=='POST':
        name=request.POST['name']
        passw=request.POST['password']
        cpass=request.POST['cpassword']
        mail=request.POST['email']
        phne=request.POST['mobile']
        usernameexists=userreg.objects.filter(username=name)
        emailexists=userreg.objects.filter(email=mail)
        if usernameexists:
            messages.error(request,"username already exsist")
        elif emailexists:
            messages.error(request,"Email already exsist")
        elif passw!=cpass:
            messages.error(request,"Password does not match")
        else:
            userreg.objects.create(username=name,password=passw,email=mail,phone=phne).save()
            return redirect("/")
    return render(request,"userregister.html")
def userlogin(request):
    if request.method=='POST':
        mail=request.POST['email']
        passw=request.POST['password']
        user=userreg.objects.filter(email=mail,password=passw)
        if user:
            request.session['email']=mail 
            return redirect("userpage")
        else:
            messages.error(request,"username and password doesnot match")
    return render(request,"userlogin.html")
def logout(request):
    del request.session['email']
    return redirect('/')
def userpage(request):
    if 'email' in request.session:
        current_user=request.session['email']
        user=userreg.objects.get(email=current_user)
        return render(request,"userpage.html",{'current_user':current_user,'user':user})
    
    return render(request,"userpage.html")
def usercomp(request):
    if 'email' in request.session:
        current_user=request.session['email']
        user=userreg.objects.get(email=current_user)
        
        if request.method=='POST':
            comparea=request.POST['rarea']
            compemail=request.POST['remail']
            compl=request.POST['rcomp']
            regcomp.objects.create(rarea=comparea,remail=compemail,rcomp=compl)
            return redirect("userpage")
        return render(request,"usercomp.html",{'current_user':current_user,'user':user})
    return render(request,"usercomp.html")
def mycomplaint(request):
    if 'email' in request.session:
        current_user=request.session['email']
        user=userreg.objects.get(email=current_user)
        complaintuser=regcomp.objects.filter(remail=user.email)
        return render(request,"mycomplaint.html",{'complaint':complaintuser})
def admin2(request):
    return render(request,"adminpage.html")
def adminlogin(request):
    adminuser="admin@gmail.com"
    pas="admin@123"
    if request.method=='POST':
        name=request.POST['email']
        passw=request.POST['password']
        if name==adminuser and passw==pas:
            request.session=name
            return redirect("admin2")
        else:
            messages.error(request,"Invalid Credentials")
    return render(request,"adminlogin.html")
def adminlogout(request):
    del request.session
    return redirect("/")
def createbin(request):
    if request.method=='POST':
        binarea=request.POST['area']
        binmark=request.POST['landmark']
        drmail=request.POST['dmail']
        cperiod=request.POST['period']
        bin.objects.create(area=binarea,landmark=binmark,dmail=drmail,period=cperiod)
        return redirect("admin2")

    return render(request,"createbin.html")
def createdriver(request):
    if request.method=='POST':
        divname=request.POST['dname']
        divpass=request.POST['dpassword']
        divemail=request.POST['demail']
        divarea=request.POST['darea']
        driver.objects.create(dname=divname,dpassword=divpass,demail=divemail,darea=divarea)
        drivstatus.objects.create(drivername=divemail,area=divarea)
        return redirect("admin2")
    return render(request,"createdriver.html")

def driverlogin(request):
    if request.method=='POST':
        dvmail=request.POST['email']
        dvpassw=request.POST['password']
        driv=driver.objects.filter(demail=dvmail,dpassword=dvpassw)
        if driv:
            request.session['demail']=dvmail
            return redirect("driver2")
        else:
            messages.error(request,"username and password doesnot match")
    return render(request,"driverlogin.html")
def driverlogout(request):
    del request.session['demail']
    return redirect("/")
def driver2(request):
    return render(request,"driverpage.html")
def viewcomplaint(request):
    details=regcomp.objects.all()
    return render(request,"viewcomplaint.html",{'details':details})
def viewcomplaint2(request,id):
    complaint=regcomp.objects.get(id=id)
    if request.method=='POST':
        status=request.POST['Status']
        complaint.status=status
        complaint.save()
    return render(request,"complaint.html",{'regcomp':complaint})
def userdetails(request):
    details=userreg.objects.all()
    return render(request,"userdetails.html",{'details':details})
def updatebin(request):
    details=bin.objects.all()
    return render(request,"bin.html",{'details':details})
def updatebin1(request,id):
    bin1=bin.objects.get(id=id)
    if request.method=='POST':
        binarea=request.POST['area']
        binmark=request.POST['landmark']
        drmail=request.POST['dmail']
        cperiod=request.POST['period']
        bin1.area=binarea
        bin1.landmark=binmark
        bin1.dmail=drmail
        bin1.period=cperiod
        bin1.save()
        return redirect("admin2")
    return render(request,"updatebin.html",{'bin':bin1})
def deletebin(request,id):
    bin1=bin.objects.get(id=id)
    bin1.delete()
    return redirect("admin2")
def deletedriver(request,id):
    driver1=driver.objects.get(id=id)
    driver1.delete()
    return redirect("admin2")

def updatedriver(request):
    details=driver.objects.all()
    return render(request,"drivers.html",{'details':details})
def updatedriver1(request,id):
    driver1=driver.objects.get(id=id)
    driver2=drivstatus.objects.get(drivername=driver1.demail,area=driver1.darea)
    if request.method=='POST':
        divname=request.POST['dname']
        divpass=request.POST['dpassword']
        divemail=request.POST['demail']
        divarea=request.POST['darea']
        driver1.dname=divname
        driver1.dpassword=divpass
        driver1.demail=divemail
        driver1.darea=divarea
        driver2.drivername=divemail
        driver2.area=divarea
        driver1.save()
        driver2.save()
        return redirect("admin2")
    return render(request,"updatedriver.html",{'driver':driver1})
def driverwork(request):
    if 'demail' in request.session:
        user=request.session['demail']
        drivermail=driver.objects.get(demail=user)
        period=bin.objects.get(dmail=drivermail.demail)
        report=drivstatus.objects.get(drivername=drivermail.demail)
        if request.method=='POST':
            status=request.POST['Status']
            report.status=status
            report.save()
            return redirect('driver2')
        return render(request,"driverwork.html",{'drivermail':drivermail,'period':period,'report':report})
def workreport(request):
    report=drivstatus.objects.all()
    return render(request,"workreport.html",{'report':report})    
