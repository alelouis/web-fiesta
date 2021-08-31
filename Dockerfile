FROM continuumio/miniconda
WORKDIR /app

COPY fiesta-back/environment.yml /app/
RUN conda env create -f environment.yml

COPY startup.sh /app/startup.sh
ADD fiesta-back /app/

EXPOSE 5000

CMD ["/bin/bash", "/app/startup.sh"]