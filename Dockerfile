FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y \
    gcc g++ libxml2-dev libxslt1-dev zlib1g-dev

RUN apt-get install -y libleveldb1 libleveldb-dev
RUN conda install -c conda-forge leveldb
RUN conda install -c conda-forge python-snappy
RUN pip install plyvel
RUN conda install jupyter -y
RUN apt-get install -y libsnappy1 libsnappy-dev
RUN pip install tqdm
RUN pip install pytest

WORKDIR /app
ADD . /app

CMD jupyter notebook --ip=0.0.0.0 --no-browser --allow-root
