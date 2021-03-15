FROM registry.access.redhat.com/ubi8/python-38

LABEL io.openshift.expose-services="8070:myflask" io.k8s.description="A basic and first my Python server based on Flask, uses BUILD. ONBUILD unfortunatelly doesnot work here" io.k8s.display-name="MyFlask Application" io.openshift.tags="flask, test, learning"

ENV APPROOT=/opt/app
CMD mkdir -pv ${APPROOT}
#ADD dictionary ${APPROOT}
ONBUILD ADD dictionary /opt/app/ 
#COPY requirements.txt /opt/app/

RUN pip install --upgrade pip && pip3 install -r /opt/app/requirements

EXPOSE 8070

RUN chgrp -R 0 /opt/app && chmod -R g=u /opt/app

RUN sed -i "s/8090/8070/g" /opt/app/app.py
#USER root
USER 1001

CMD ["nohup", "python", "/opt/app/app.py", "&"]
#CMD ["nohup", "python", "/opt/app/app_env_vars.py", "&"]

