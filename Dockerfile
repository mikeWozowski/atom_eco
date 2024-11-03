FROM python:3.11

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

COPY . .

EXPOSE 8000

CMD ["pipenv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]