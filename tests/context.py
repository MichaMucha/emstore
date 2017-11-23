# -*- coding: utf-8 -*-

import os
import sys

import emstore
from emstore import glove

MODULE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEST_DB_PATH = os.path.join(MODULE_PATH, 'tests', 'test_db')
SAMPLE_DATA = os.path.join(MODULE_PATH, 'tests', 'glove_sample')

sys.path.insert(0, MODULE_PATH)
