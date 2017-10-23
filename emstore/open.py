from contextlib import contextmanager
from inspect import currentframe, getargvalues

import plyvel


@contextmanager
def open_leveldb(name,
                 create_if_missing=False,
                 error_if_exists=False,
                 paranoid_checks=None,
                 write_buffer_size=None,
                 max_open_files=None,
                 lru_cache_size=None,
                 block_size=None,
                 block_restart_interval=None,
                 compression='snappy',
                 bloom_filter_bits=0,
                 comparator=None,
                 comparator_name=None):
    """Context manager for plyvel leveldb interface.

    See plyvel.DB.__init__ documentation to learn more about args.
    """
    _, _, _, kwargs = getargvalues(currentframe())
    db = plyvel.DB(**kwargs)
    try:
        yield db
    finally:
        db.close()
