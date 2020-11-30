FROM continuumio/miniconda

COPY . /usr/local/src/Views_dir
WORKDIR /usr/local/src/Views_dir
RUN wget -O - https://world-modelers.s3.amazonaws.com/data/views2/storage/data.zip | wc -l > /number
RUN echo 'unzip data.zip -d /usr/local/src/Views_dir/storage/'
RUN ./install_views2.sh
RUN echo "source activate views2"
ENV PATH /opt/conda/envs/views2/bin:$PATH



ENTRYPOINT ["python3", "projects/model_development/sb_ensemble_script.py"]
CMD ["--start_date 483", "--end_date 520"]