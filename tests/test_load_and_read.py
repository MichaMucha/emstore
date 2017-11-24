# -*- coding: utf-8 -*-

import os
import unittest
from subprocess import call

from .context import SAMPLE_DATA, TEST_DB_PATH, emstore


class LoadAndReadTestSuite(unittest.TestCase):
    """Test loading a repository and getting keys."""

    def setUp(self):
        super().setUp()
        emstore.create_embedding_database(
            os.path.join(SAMPLE_DATA, 'glove_1000.zip'),
            TEST_DB_PATH,
            datasize=1000,
            overwrite=True)

    def test_open(self):
        with emstore.Emstore(TEST_DB_PATH) as embeddings:
            print(emstore.Emstore.__doc__)
            self.assertFalse(embeddings.closed)
            print(embeddings)

    def test_read(self):
        with emstore.Emstore(TEST_DB_PATH) as embeddings:
            print(embeddings['the'])

    def tearDown(self):
        call(['rm', '-rf', TEST_DB_PATH])


if __name__ == '__main__':
    unittest.main()
