# -*- coding: utf-8 -*-

import os
import unittest
from subprocess import call
import requests

from .context import emstore
from .context import glove
from .context import emstore

TEST_GLOVE_DIR = os.path.join('/', 'tmp', 'glove')


class DownloadGloveTestSuite(unittest.TestCase):
    """Downlad glove test cases."""

    def setUp(self):
        super().setUp()
        try:
            os.makedirs(TEST_GLOVE_DIR)
        except FileExistsError:
            pass

    def test_download_fn(self):
        try:
            requests.get('www.google.com')
        except Exception:
            return
        test_url = 'https://nlp.stanford.edu/pubs/glove.pdf'
        test_target_path = os.path.join(TEST_GLOVE_DIR, 'test.pdf')
        emstore.glove.download(target_path=test_target_path, url=test_url)
        self.assertTrue(os.path.exists(test_target_path))

    def test_download_glove1000(self):
        try:
            requests.get('www.google.com')
        except Exception:
            return
        test_url = ('https://github.com/MichaMucha/' +
                    'emstore/raw/master/tests/glove_sample/glove_1000.zip')
        test_target_path = os.path.join(TEST_GLOVE_DIR, 'glove.zip')
        emstore.glove.download(target_path=test_target_path, url=test_url)
        self.assertTrue(os.path.exists(test_target_path))

    def test_create_glove(self):
        try:
            requests.get('www.google.com')
        except Exception:
            return
        test_target_path = os.path.join(TEST_GLOVE_DIR, 'glove.zip')
        test_db_path = os.path.join(TEST_GLOVE_DIR, 'test_db')
        emstore.glove.create(
            embeddings_file=test_target_path, path_to_db=test_db_path)
        self.assertTrue(os.path.exists(test_db_path))
        embeddings = emstore.Emstore(test_db_path)
        self.assertFalse(embeddings.closed)
        embeddings.close()

    def tearDown(self):
        call(['rm', '-rf', TEST_GLOVE_DIR])


if __name__ == '__main__':
    unittest.main()
