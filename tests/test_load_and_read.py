# -*- coding: utf-8 -*-

import unittest
from subprocess import call

from .context import TEST_DB_PATH, emstore


class LoadAndReadTestSuite(unittest.TestCase):
    """Test loading a repository and getting keys."""

    def setUp(self):
        super().setUp()
        emstore.create_embedding_database(
            'glove_sample/glove_1000.zip',
            TEST_DB_PATH,
            datasize=1000,
            overwrite=True)

    def test_open(self):
        self.embeddings = emstore.Emstore(TEST_DB_PATH)
        print(emstore.Emstore.__doc__)
        self.assertFalse(emstore.closed)
        print(self.embeddings)

    def test_read(self):
        self.embeddings = emstore.Emstore(TEST_DB_PATH)
        print(self.embeddings['the'])

    def tearDown(self):
        call(['rm', '-rf', TEST_DB_PATH])


if __name__ == '__main__':
    unittest.main()
