# python image
FROM python:3.8

# set working directory for app
WORKDIR /usr/src/app

# copy all files to container WORKDIR
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# port number container should expose
EXPOSE 8080

# run the commands
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app", "--timeout", "600"]  
# CMD ["python", "app.py"]