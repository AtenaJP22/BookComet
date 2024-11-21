# syntax=docker/dockerfile:1

FROM python:3.11

 WORKDIR /code

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5001

# ENTRYPOINT ["gunicorn", "app:app"]
# ENV FLASK_APP=app.py
# CMD ["flask", "run", "--host", "0.0.0.0"]
CMD ["python", "app.py"]