from inspect import currentframe, getargvalues

import plyvel


class Emstore(object):
    """docstring for Emstore"""

    def __init__(
            self,
            path,
            #  create_if_missing=False,
            #  error_if_exists=False,
            #  paranoid_checks=None,
            #  write_buffer_size=None,
            #  max_open_files=None,
            #  lru_cache_size=None,
            #  block_size=None,
            #  block_restart_interval=None,
            #  compression='snappy',
            #  bloom_filter_bits=0,
            #  comparator=None,
            #  comparator_name=None
    ):
        super(Emstore, self).__init__()
        _, _, _, kwargs = getargvalues(currentframe())
        name = kwargs['path']
        self.path = name
        kwargs = {
            k: v
            for k, v in kwargs.items()
            if k in [
                'create_if_missing', 'error_if_exists', 'paranoid_checks',
                'write_buffer_size', 'max_open_files', 'lru_cache_size',
                'block_size', 'block_restart_interval', 'compression',
                'bloom_filter_bits', 'comparator', 'comparator_name'
            ]
        }
        self.db = plyvel.DB(name, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __str__(self):
        return """<Emstore path:{} lock:{}>""".format(self.path,
                                                      not self.closed)

    def __getitem__(self, key):
        return _read(key, self.db)

    def __iter__(self):
        pass

    def __contains__(self, item):
        pass

    def __len__(self):
        pass

    def close(self):
        self.db.close()

    def closed():
        doc = "The closed property."

        def fget(self):
            return self.db.closed

        def fset(self, value):
            pass

        def fdel(self):
            pass

        return locals()

    closed = property(**closed())


def _read(key, db):
    """Read from leveldb and return array of floats.
    """
    key = key.encode('utf8')
    embedding = db.get(key)
    embedding.split(b' ')
    return [float(e) for e in embedding]
