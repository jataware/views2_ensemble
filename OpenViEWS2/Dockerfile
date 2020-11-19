FROM continuumio/miniconda

COPY . /usr/local/src/Views_dir
WORKDIR /usr/local/src/Views_dir

RUN ./install_views2.sh
RUN echo "source activate views2" > ~/.bashrc
ENV PATH /opt/conda/envs/views2/bin:$PATH

RUN echo "python3 projects/model_development/cflong_script.py"> ~/.bashrc