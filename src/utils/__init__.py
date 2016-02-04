#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Deepin Technology Co., Ltd.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

import sys
from cStringIO import StringIO
from contextlib import contextmanager

@contextmanager
def no_error_output():
        _stderr = sys.stderr
        sys.stderr = StringIO()
        yield
        sys.stderr = _stderr
