FROM python:3.8-alpine
RUN python -m pip install --upgrade pip

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY gestao_varejo/ /app/

ENV PYTHONUNBUFFERED=1
WORKDIR /app

CMD python /app/manage.py runserver