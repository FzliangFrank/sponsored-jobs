FROM continuumio/miniconda3
COPY requirements.txt /tmp/
COPY ./2024-02-02_-_Worker_and_Temporary_Worker.csv app/2024-02-02_-_Worker_and_Temporary_Worker.csv
COPY ./app.py app/app.py
WORKDIR "/app"
RUN conda install --file /tmp/requirements.txt
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
EXPOSE 8050