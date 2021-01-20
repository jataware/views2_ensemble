FROM continuumio/miniconda

COPY . /usr/local/src/Views_dir
WORKDIR /usr/local/src/Views_dir

RUN ./install_views2.sh
RUN echo "source activate views2"  
RUN apt-get update && apt-get install -y unzip



ENV PATH /opt/conda/envs/views2/bin:$PATH


ENTRYPOINT ["python3", "projects/model_development/sb_ensemble.py"]
CMD ["--start_date 483", "--end_date 520", '--country "All"' , "--gdp_pcap 0", "--infant_mortality 0" , "--liberalDemocracyIndex 0", "--foodProdIndex 0" ]
