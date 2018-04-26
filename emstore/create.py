# -*- coding: utf-8 -*-

import os
import struct
from functools import partial
from contextlib import contextmanager
from functools import partial
from io import BufferedReader, UnsupportedOperation
from subprocess import call
from zipfile import BadZipFile, ZipFile

from tqdm import tqdm

from emstore.open import open_leveldb

STRUCT_FORMAT = 'e'


class VecIOWrapper(BufferedReader):
    def __init__(self, *args, vector_size=None, fasttext_format=False, **kwargs):
        super().__init__(*args, **kwargs)
        if vector_size is None:
            try:
                vector_size, fasttext_format = self.infer_vector_size()
            except UnsupportedOperation:
                raise Exception(
                    '''Unable to infer vector size without read loss.
                    Please specify vector size''')
        self.vector_size = vector_size
        self.pack = struct.Struct(str(vector_size) + STRUCT_FORMAT).pack
        if fasttext_format:
            # pass first line
            super().__next__()

    def __next__(self):
        line = super().__next__()[:-1]  # read and drop newline char
        x = line.split(b' ')  # split by whitespace
        if len(x) > self.vector_size + 1:
            k, v = b''.join(x[:-self.vector_size]), x[-self.vector_size:]
        else:
            k, v = x[0], x[1:]
        v = [float(f) for f in v]
        return k, self.pack(*v)

    def infer_vector_size(self):
        # sample 1 entry
        first_line = super().readline()
        first_line = first_line.split(b' ')
        fasttext_format = False
        if len(first_line) == 2:
            # could be a fasttext format file - read another line
            first_line = super().readline()
            first_line = first_line.split(b' ')
            fasttext_format = True
        self.seek(0)
        return len(first_line) - 1, fasttext_format


@contextmanager
def open_embeddings_file(path, vector_size=None, archive_file=None):
    """Universal context manager to open CSV-like files with word embeddings.

    Returns a file-like object (BufferedReader subclass).

    Accepts both compressed and uncompressed files.

    Infers vector size if not specified, and matches all vectors to that size.

    If path is an archive that contains multiple files,
    please specify archive_file.
    """
    try:
        archive = ZipFile(path)
        filenames = [f.filename for f in archive.filelist]
        if len(filenames) == 0:
            raise Exception('Empty archive.')
        elif archive_file is not None:
            file = archive_file
        elif len(filenames) == 1:
            file = filenames[0]
        elif len(filenames) > 1:
            raise Exception('\n'.join([
                'Multiple files in archive.',
                'Please specify the archive_file argument.', 'Available files:'
            ] + filenames))
        open_f = archive.open
        if vector_size is None:
            with open_f(file) as g:
                # sample 1 entry
                first_line = g.readline()
                first_line = first_line.split(b' ')
                fasttext_format = False
                if len(first_line) == 2:
                    # could be a fasttext format file - read another line
                    first_line = g.readline()
                    first_line = first_line.split(b' ')
                    fasttext_format = True
            vector_size = len(first_line) - 1
    except BadZipFile:
        file = path
        open_f = partial(open, mode='rb')

    with open_f(file) as g:
        yield VecIOWrapper(g, vector_size=vector_size, 
            fasttext_format=fasttext_format)


def create_embedding_database(embeddings_file,
                              path_to_database,
                              datasize=None,
                              overwrite=False):
    """Create embedding store in leveldb.
    
    Arguments:
        embeddings_file {str} --  path to downloaded GloVe embeddings. 'None'
            will trigger download
        path_to_database {str} -- Destination - where to create the embeddings     database. 'None' by default - builds in ~/glove
    
    Keyword Arguments:
        datasize {int} -- number of lines if you want to see a progress bar when loading from a zip file (default: {None})
        overwrite {bool} -- [description] (default: {False})
    """


    
    if overwrite:
        if os.path.exists(path_to_database):
            call(['rm', '-rf', path_to_database])
    if not os.path.exists(path_to_database):
        os.makedirs(path_to_database)
    with open_leveldb(
            path_to_database,
            create_if_missing=True,
            error_if_exists=not overwrite) as db:
        leveldb_write_batch = 256
        i = 0
        batch = db.write_batch()
        with open_embeddings_file(embeddings_file) as a:
            for key, embedding in tqdm(a, total=datasize):
                i += 1
                batch.put(key, embedding)
                if i % leveldb_write_batch == 0:
                    batch.write()
                    batch = db.write_batch()
            batch.write()
