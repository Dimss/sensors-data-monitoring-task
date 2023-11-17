FROM python:3.11
ENV PYTHONPATH=/opt/app-root
WORKDIR /opt/app-root
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY alert_service alert_service/
COPY config config/
COPY main_service main_service/
COPY queue_impl queue_impl/
COPY sensors sensors/
COPY main.py main.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt