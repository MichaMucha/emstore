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

    def test_the(self):
        embeddings = emstore.Emstore(TEST_DB_PATH)
        the = embeddings['the']
        self.assertEqual(len(the), 300)
        self.assertEqual(the[10], -0.35179)
        self.assertEqual(the[73], 0.17856)
        self.assertEqual(the[299], 0.1323)
        embeddings.close()

    def test_about(self):
        embeddings = emstore.Emstore(TEST_DB_PATH)
        about = embeddings['about']
        self.assertEqual(len(about), 300)
        self.assertEqual(about[231], 0.26429)
        self.assertEqual(about[45], 0.34683)
        embeddings.close()

    def test_people(self):
        embeddings = emstore.Emstore(TEST_DB_PATH)
        people = embeddings['people']
        self.assertEqual(len(people), 300)
        self.assertEqual(people[163], 0.22873)
        self.assertEqual(people[11], 0.070743)
        embeddings.close()

    def tearDown(self):
        call(['rm', '-rf', TEST_DB_PATH])


if __name__ == '__main__':
    unittest.main()
