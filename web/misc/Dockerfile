FROM python:3
WORKDIR /web
ENV FLASK_APP=__init__.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
COPY requirement.txt requirement.txt
RUN pip install --no-cache-dir -r requirement.txt
EXPOSE 5000
COPY .. .
CMD ["flask", "run"]
