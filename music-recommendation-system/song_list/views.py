# Create your views here.
from django.shortcuts import render
import mysql.connector
import webbrowser

def musiclistaction(request):
    m = mysql.connector.connect(host="localhost", user="root", passwd="", database='mediconnectdb')
    cursor = m.cursor()
    c = "select * from file1 "
    cursor.execute(c)
    Result = cursor.fetchall()
    return render(request, "music_list.html", {'data':Result})
