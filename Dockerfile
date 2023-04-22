FROM python:3.10.10-bullseye

WORKDIR /project

COPY extension.txt extension.txt

RUN pip install -r extension.txt

COPY . .


ENV FLASK_APP=app/app.py
ENV PYTHONPATH=/project
CMD ["python", "-m", "flask", "run","src.app:app","--host=0.0.0.0"] 


