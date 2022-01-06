# -*- coding: utf-8 -*-
#
# parnia/common/__init__.py
#

"""
Provide application functionality.
"""

import string

from .key_generator import KeyGenerator

__all__ = (
    'generate_public_key',
    )


def generate_public_key():
    gen = KeyGenerator(length=20)
    return gen.generate()


