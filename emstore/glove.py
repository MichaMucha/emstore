import os
import warnings
from subprocess import call

import requests
from tqdm import tqdm

from .create import create_embedding_database

DEFAULT_GLOVE_DOWNLOAD_PATH = os.path.join('/', 'tmp', 'glove', 'glove.zip')


def download(target_path=None, url=None):
    """Download GloVe Common Crawl 840B tokens.

    (840B tokens, 2.2M vocab, cased, 300d vectors, 2.03 GB download)

    args:
        target_path: where to save
        default /tmp/glove/glove.zip

        url: where to downlad from
        default http://nlp.stanford.edu/data/glove.840B.300d.zip

    """
    if target_path is None:
        target_path = DEFAULT_GLOVE_DOWNLOAD_PATH
        try:
            os.makedirs(os.path.dirname(DEFAULT_GLOVE_DOWNLOAD_PATH))
        except FileExistsError:
            pass
    if url is None:
        url = 'http://nlp.stanford.edu/data/glove.840B.300d.zip'
    response = requests.get(url, stream=True)
    with open(target_path, 'wb') as f:
        pbar = tqdm(
            unit="KB", total=int(response.headers['Content-Length']) // 1024)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                pbar.update(len(chunk) // 1024)
                f.write(chunk)


def create(embeddings_file=None, path_to_db=None, keep_file=True):
    if embeddings_file is None:
        if os.path.exists(DEFAULT_GLOVE_DOWNLOAD_PATH):
            embeddings_file = DEFAULT_GLOVE_DOWNLOAD_PATH
        else:
            warnings.warn('''GloVe embeddings file path not specified,
            archive not found at default path.
            Commencing 2.03GB download.
            File will be deleted after DB is created.
            //default path is:
            {}
            '''.format(DEFAULT_GLOVE_DOWNLOAD_PATH))
            download()
            embeddings_file = DEFAULT_GLOVE_DOWNLOAD_PATH
            keep_file = False
    if path_to_db is None:
        path_to_db = os.path.expanduser(os.path.join('~', 'glove'))

    create_embedding_database(embeddings_file, path_to_db)
    if keep_file is False:
        call(['rm', '-f', embeddings_file])
