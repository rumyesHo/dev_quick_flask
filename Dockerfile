FROM registry.access.redhat.com/ubi8/python-38

ENV APPROOT=/opt/app
CMD mkdir -pv ${APPROOT}
ADD dictionary ${APPROOT}
#ONBUILD ADD dictionary /opt/app/ 
#COPY requirements.txt /opt/app/

RUN pip install --upgrade pip && pip3 install -r /opt/app/requirements

EXPOSE 8090

USER root
CMD ["nohup", "python", "/opt/app/app.py", "&"]
#CMD ["nohup", "python", "/opt/app/app_env_vars.py", "&"]

