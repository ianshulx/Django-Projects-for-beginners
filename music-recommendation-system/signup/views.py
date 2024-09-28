from django.shortcuts import render

# Create your views here.
import mysql.connector


fn = ''
ln = ''
em = ''
pwd = ''

def signaction(request):
    global fn, ln, s, em, pwd
    if request.method == "POST":
        m = mysql.connector.connect(host="localhost", user="root", passwd="", database='mediconnectdb')
        cursor = m.cursor()
        d = request.POST
        for key, value in d.items():
            if key == "first_name":
                fn = value
            if key == "last_name":
                ln = value
            if key == "email":
                em = value
            if key == "password":
                pwd = value

        c = "insert into user Values('{}','{}','{}','{}')".format(fn, ln, em, pwd)
        cursor.execute(c)
        m.commit()
    

    return render(request, 'signup_page.html')