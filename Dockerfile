FROM registry.access.redhat.com/ubi8/python-38

CMD mkdir -pv /opt/app
ADD dictionary /opt/app/ 
#COPY requirements.txt /opt/app/

RUN pip install --upgrade pip && pip3 install -r /opt/app/requirements.txt

EXPOSE 8090

#CMD ["nohup", "python", "/opt/app/app.py", "&"]
CMD ["nohup", "python", "/opt/app/app_env_vars.py", "&"]

