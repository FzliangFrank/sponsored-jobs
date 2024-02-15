FROM continuumio/miniconda3
COPY requirements.txt /tmp/
COPY ./app.py app/app.py
COPY ./.env app/.env
WORKDIR "/app"
RUN conda install --file /tmp/requirements.txt
ENTRYPOINT ["python3" ]
CMD [ "app.py" ]
EXPOSE 8050