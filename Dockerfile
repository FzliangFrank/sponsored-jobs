FROM python:3.11
COPY requirements.txt /tmp/
COPY ./app.py app/app.py
COPY ./tools.py app/tools.py
#COPY ./.env app/.env
# ADD app/assets ./assets 
WORKDIR "/app"
RUN pip install -r /tmp/requirements.txt
ENTRYPOINT ["python3" ]
CMD [ "app.py" ]
EXPOSE 8080