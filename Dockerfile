FROM python:3

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=1000

EXPOSE 1000

ENTRYPOINT [ "flask" ]
CMD [ "run" ]