from django.shortcuts import render

# Create your views here.
import mysql.connector


fi = ''
la = ''
el = ''
sb = ''

def contactaction(request):
    global fi, la, el,sb
    if request.method == "POST":
        m = mysql.connector.connect(host="localhost", user="root", passwd="", database='music')
        cursor = m.cursor()
        d = request.POST
        for key, value in d.items():
            if key == "firstname":
                fi = value
            if key == "lastname":
                la = value
            if key == "email":
                el = value
            if key == "subject":
                sb = value

        c = "insert into contact_us Values('{}','{}','{}','{}')".format(fi, la, el,sb)
        cursor.execute(c)
        m.commit()
    

    return render(request, 'contactus.html')