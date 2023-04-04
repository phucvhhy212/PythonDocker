FROM python:3.10.10-bullseye

WORKDIR /app

COPY extension.txt extension.txt

RUN pip install -r extension.txt

COPY . .

CMD ["python", "-m", "flask", "run","--host=0.0.0.0"]