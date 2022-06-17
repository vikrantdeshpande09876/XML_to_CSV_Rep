FROM python:3.6.12-alpine

RUN mkdir /XML_TO_CSV_REP
WORKDIR /XML_TO_CSV_REP/
COPY . .

RUN pip install gunicorn
RUN pip install -e .

ENV FLASK_APP xml_to_csv
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 5000

# Run Flask command
CMD ["gunicorn", "-b", "0.0.0.0:5000", '"xml_to_csv:create_app()"']