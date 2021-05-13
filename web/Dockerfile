FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=__init__.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirement.txt requirement.txt
RUN pip install -r requirement.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]