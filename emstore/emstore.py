class Emstore(object):
    """docstring for Emstore"""

    def __init__(self, arg):
        super(Emstore, self).__init__()
        self.arg = arg

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __str__(self):
        pass

    def __getitem__(self, key):
        pass

    def __iter__(self):
        pass

    def __contains__(self, item):
        pass

    def __len__(self):
        pass


def _read(key, db):
    """Read from leveldb and return array of floats.

    key.encode('utf8')
    embedding = db.get(key)
    embedding.split(b' ')
    return [float(e) for e in embedding]

    """
