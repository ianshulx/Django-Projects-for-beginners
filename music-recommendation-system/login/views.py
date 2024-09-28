from django.shortcuts import render
import mysql.connector

# Create your views here.
em = ''
pwd = ''


# Create your views here.
def loginaction(request):
    global em, pwd
    if request.method == "POST":
        m = mysql.connector.connect(host="localhost", user="root", passwd="", database='mediconnectdb')
        cursor = m.cursor()
        d = request.POST
        for key, value in d.items():
            if key == "email":
                em = value
            if key == "password":
                pwd = value

        c = "select * from user where email='{}' and password='{}'".format(em, pwd)
        cursor.execute(c)
        t = tuple(cursor.fetchall())
        if t == ():
            return render(request, 'error.html')
        else:
            return render(request, "menu.html")


    return render(request, '2.html')