FROM python:3.5
MAINTAINER Kenta Mukai

ENV app_name meshi-tero-bot
ENV app_dir /var/apps/$app_name

RUN mkdir -p $app_dir
COPY ./$app_name/requirements.txt $app_dir
RUN pip install -r $app_dir/requirements.txt
COPY ./$app_name $app_dir
WORKDIR $app_dir

EXPOSE 3031
CMD exec /usr/local/bin/uwsgi ${app_dir}/uwsgi.ini
