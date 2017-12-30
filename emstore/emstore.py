from functools import lru_cache, partial
from inspect import currentframe, getargvalues

import plyvel
import struct

STRUCT_FORMAT = 'e'

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
        db = plyvel.DB(name, **kwargs)
        vector = struct.iter_unpack(STRUCT_FORMAT, next(db.__iter__())[1])
        vector_size = len(list(vector))
        self.vector_size = vector_size
        db.close()
        self.db = plyvel.DB(name, **kwargs)
        self.unpack = struct.Struct(str(vector_size) + STRUCT_FORMAT).unpack

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __str__(self):
        return """<Emstore path:{} lock:{}>""".format(self.path,
                                                      not self.closed)

    @lru_cache(maxsize=1024)
    def __getitem__(self, key):
        return self.__read(key)

    def __iter__(self):
        # return self.db.__iter__()
        with self.db.iterator() as it:
            for k, v in it:
                yield k.decode('utf-8'), self.unpack(v)

    def keys(self):
        with self.db.iterator(include_value=False) as it:
            for key in it:
                yield key.decode('utf-8')

    def values(self):
        with self.db.iterator(include_key=False) as it:
            for value in it:
                yield self.unpack(value)

    def __contains__(self, item):
        pass

    def __len__(self):
        pass

    def __read(self, key):
        """Read from leveldb and return array of floats.
        """
        key = key.encode('utf8')
        try:
            val = self.unpack(self.db.get(key))
        except TypeError:
            val = [0.] * self.vector_size
        return val


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
