# -*- coding: utf-8 -*-


MAJOR = 0
MINOR = 1
PATCH = 0
DEV = True

VERSION = '{}.{}.{}'.format(MAJOR, MINOR, PATCH)
if DEV:
    VERSION += '.dev'
