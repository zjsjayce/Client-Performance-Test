#!/usr/bin/env python
# -*- coding: utf-8 -*-

class CaseInitException(Exception):
    def __init__(self, message, cause):
        super(CaseInitException, self).__init__(message + ', caused by ' + repr(cause))
        self.cause = cause

class CaseExecutingException(Exception):
    def __init__(self, message, cause):
        super(CaseExecutingException, self).__init__(message + ', caused by ' + repr(cause))
        self.cause = cause