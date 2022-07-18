# base image  
FROM python:3.8   
# setup environment variable  

COPY ./requirements.txt /requirements.txt
COPY . /contact
COPY ./scripts /scripts

WORKDIR /contact
EXPOSE 8000

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# install dependencies  
RUN pip install --upgrade pip  

# run this command to install all dependencies
RUN pip install -r requirements.txt  
# port where the Django app runs  
EXPOSE 8000  
# start server  
#ENV PATH="/scripts:/py/bin:$PATH"
#
#CMD ["run.sh"]