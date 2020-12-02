FROM continuumio/miniconda

COPY . /usr/local/src/Views_dir
WORKDIR /usr/local/src/Views_dir

RUN ./install_views2.sh
RUN echo "source activate views2"  
RUN apt-get update && apt-get install -y unzip
RUN wget -O tables.zip https://world-modelers.s3.amazonaws.com/data/views2/storage/tables.zip | wc -l > /number &&\
    unzip /usr/local/src/Views_dir/tables.zip -d /usr/local/src/Views_dir/storage/data/ &&\
    rm -rf /usr/local/src/Views_dir/tables.zip &&\
    wget -O data.zip https://world-modelers.s3.amazonaws.com/data/views2/storage/data.zip | wc -l > /number &&\
    unzip /usr/local/src/Views_dir/data.zip -d /usr/local/src/Views_dir/ &&\
    rm -rf /usr/local/src/Views_dir/data.zip

ENV PATH /opt/conda/envs/views2/bin:$PATH



ENTRYPOINT ["python3", "projects/model_development/sb_ensemble_script.py"]
CMD ["--start_date 483", "--end_date 520"]
