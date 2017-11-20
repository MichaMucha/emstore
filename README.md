# `emstore`

**fast word embedding lookup with reduced memory footprint and loading time**

>**Powered by LevelDB**

Tired of word embeddings loading for 5 minutes on script startup?
Not excited about having all your RAM eaten up?
Still want fast lookup?

**Get `emstore`!**

## Key Features

* Easily initialize indexed word embedding databases on disk. Automatic vector size detection.
* Create databases from whitespace-separated text files (reading ZIP archives supported) without hassle
* Lazy-load embeddings instead of reading the entire file on startup.
* LRU caching (1024 last words by default)
* Support for downloading GloVe embeddings
* Emstore handles LevelDB locks and bytes IO for you

Create Emstore word embeddings indexed LevelDB:
```Python
>>> import emstore
>>> emstore.create_embedding_database(
        '/app/tests/glove_sample/glove_1000.zip', 
        '~/glove', 
        overwrite=True)
1000it [00:00, 29874.17it/s]
```

Open Emstore word embeddings DB
```Python
>>> from emstore import Emstore
>>> e = Emstore('~/glove')
>>> e['the']
[0.27204,
 -0.06203,
 -0.1884,
 0.023225,
 -0.018158,
 0.0067192,
 ...
]
```

Also as context to release lock automatically:
```Python
>>> with Emstore('~/glove') as e:
>>>     the = e['the']
>>> the
[0.27204,
 -0.06203,
 -0.1884,
 0.023225,
 -0.018158,
 0.0067192,
 ...
]
```

Download and create GloVe word embeddings db
```Python
>>> from emstore import glove
>>> glove.create(
        embeddings_file=None, # path to downloaded GloVe embeddings. 'None' will trigger download
        path_to_db=None # Destination - where to create the embeddings database. 'None' by default - builds in ~/glove
)
/app/emstore/glove.py:55: UserWarning: GloVe embeddings file path not specified,
archive not found at default path.
Commencing 2.03GB download.
File will be deleted after DB is created.
default download path is:
/tmp/glove/glove.zip

  1%|▍                                | 29594/2125750 [00:17<09:06, 3832.52KB/s]
```

## Installing

#### Linux

You'll need leveldb

```
apt-get update && apt-get install -y \
    gcc g++ libxml2-dev libxslt1-dev zlib1g-dev
apt-get install -y libleveldb1 libleveldb-dev
```
Requirements and emstore:
```
pip install -r requirements.txt
python setup.py install
```

Also see included docker-compose and Dockerfile.

## Dependencies

This software is made possible thanks to:

- [LevelDB](http://leveldb.org/)
- [Plyvel](https://github.com/wbolster/plyvel/)

## More about GloVe word vectors:

- [GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/projects/glove/)

## Contributing

This is an early release. 
Your feedback and use cases will be appreciated.

feel free to contribute improvements as well. Some ideas:
 - simplify installation (conda build)
 - docs
 - performance enhancements
 - use cases
 - managing lock so that multiple docker containers can map volume to one db
 

#### License: MIT


> Twitter [@jeremimucha](https://twitter.com/jeremimucha)
