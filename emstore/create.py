# -*- coding: utf-8 -*-

import os
from contextlib import contextmanager
from functools import partial
from io import BufferedReader, UnsupportedOperation
from subprocess import call
from zipfile import BadZipFile, ZipFile

from tqdm import tqdm

from emstore.open import open_leveldb


class VecIOWrapper(BufferedReader):
    def __init__(self, *args, vector_size=None, **kwargs):
        super().__init__(*args, **kwargs)
        if vector_size is None:
            try:
                vector_size = self.infer_vector_size()
            except UnsupportedOperation:
                raise Exception(
                    '''Unable to infer vector size without read loss.
                    Please specify vector size''')
        self.vector_size = vector_size

    def __next__(self):
        line = super().__next__()[:-1]  # read and drop newline char
        x = line.split(b' ')  # split by whitespace
        if len(x) > self.vector_size + 1:
            return [b''.join(x[:-self.vector_size])], b' '.join(
                x[-self.vector_size:])
        else:
            return x[0], b' '.join(x[1:])

    def infer_vector_size(self):
        # sample 1 entry
        first_line = super().readline()
        first_line.split(b' ')
        self.seek(0)
        return len(first_line) - 1


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
            vector_size = len(first_line) - 1
    except BadZipFile:
        file = path
        open_f = partial(open, mode='rb')

    with open_f(file) as g:
        yield VecIOWrapper(g, vector_size=vector_size)


def create_embedding_database(embeddings_file,
                              path_to_database,
                              datasize=None,
                              overwrite=False):
    """Create embedding store in leveldb."""
    if overwrite:
        if os.path.exists(path_to_database):
            call(['rm', '-rf', path_to_database])
    with open_leveldb(
            path_to_database,
            create_if_missing=overwrite,
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
