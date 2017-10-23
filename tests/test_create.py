# -*- coding: utf-8 -*-

import unittest
from subprocess import call

from .context import TEST_DB_PATH, emstore


class CreateLevelDBTestSuite(unittest.TestCase):
    """Test loading a repository and getting keys."""

    def setUp(self):
        super().setUp()
        pass

    def test_create_from_txt(self):
        emstore.create_embedding_database(
            'glove_sample/glove_1000.txt',
            TEST_DB_PATH,
            datasize=1000,
            overwrite=True)

    def test_create_from_zip_archive(self):
        emstore.create_embedding_database(
            'glove_sample/glove_1000.zip',
            TEST_DB_PATH,
            datasize=1000,
            overwrite=True)

    def tearDown(self):
        call(['rm', '-rf', TEST_DB_PATH])


if __name__ == '__main__':
    unittest.main()
