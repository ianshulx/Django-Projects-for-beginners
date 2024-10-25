#base image

From python:3.13.0

#working directory

WORKDIR /app

#copy code

COPY . .

#requirement libraries

RUN pip install -r requirements.txt

#run libraries

#RUN python3 manage.py runserver

#cmd

CMD ["python3","manage.py","runserver","0.0.0.0:8000"]
