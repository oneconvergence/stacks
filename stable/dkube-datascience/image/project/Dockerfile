FROM ocdr/dkube-datascience-tf-cpu:v2.6.0-10
USER root
RUN pip3 install ptvsd==4.3.0

ENV PRODUCTION=true

COPY . /project
WORKDIR /project/user-app

ENV PATH="/project:${PATH}"
ENV PYTHONPATH=/opt/dkube/program:/opt/dkube

CMD ["python3", "app.py"]
EXPOSE 5678
