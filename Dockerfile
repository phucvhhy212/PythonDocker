FROM python:3.10.10-bullseye

WORKDIR /project

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "flask", "run"]



