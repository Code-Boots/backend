# 
FROM python:3.11

# 
WORKDIR /code

# 
RUN pip install poetry

# 
COPY . .

RUN poetry config installer.max-workers 10

RUN poetry install

EXPOSE ${PORT}


CMD ["sh","-c","poetry run serve-prod"]
