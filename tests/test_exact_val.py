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
        with emstore.Emstore(TEST_DB_PATH) as embeddings:
            the = embeddings['the']
            self.assertAlmostEqual(len(the), 300)
            self.assertAlmostEqual(the[10], -0.35179)
            self.assertAlmostEqual(the[73], 0.17856)
            self.assertAlmostEqual(the[299], 0.1323)

    def test_about(self):
        with emstore.Emstore(TEST_DB_PATH) as embeddings:
            about = embeddings['about']
            self.assertAlmostEqual(len(about), 300)
            self.assertAlmostEqual(about[231], 0.26429)
            self.assertAlmostEqual(about[45], 0.34683)

    def test_people(self):
        with emstore.Emstore(TEST_DB_PATH) as embeddings:
            people = embeddings['people']
            self.assertAlmostEqual(len(people), 300)
            self.assertAlmostEqual(people[163], 0.22873)
            self.assertAlmostEqual(people[11], 0.070743)

    def tearDown(self):
        call(['rm', '-rf', TEST_DB_PATH])


if __name__ == '__main__':
    unittest.main()
