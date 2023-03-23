# SPDX-License-Identifier: 0BSD
# Copyright 2017 Alexander Kozhevnikov <mentalisttraceur@gmail.com>

from sys import modules as _modules

from robot.api import logger as _logger
from robot.api import SkipExecution as _SkipExecution


__all__ = ('depends_on_test', 'depends_on_suite')
__version__ = '4.0.1'


ROBOT_LISTENER_API_VERSION = 3
ROBOT_LIBRARY_LISTENER = _modules[__name__]


_test_status_map = {}
_suite_status_map = {}


def start_test(test, result):
    _test_status_map[test.name.lower()] = Ellipsis


def end_test(test, result):
    _test_status_map[test.name.lower()] = result.status


def start_suite(suite, result):
    _suite_status_map[suite.name.lower()] = Ellipsis


def end_suite(suite, result):
    _suite_status_map[suite.name.lower()] = result.status


def _depends_on(status_map, dependency_type, name):
    message = 'Dependency not met: ' + dependency_type + ' ' + repr(name)
    status = status_map.get(name.lower(), None)
    if status is None:
        _logger.warn(message + ' not found.')
        return
    if status is Ellipsis:
        _logger.warn(message + ' mid-execution.')
        return
    if status == 'PASS':
        return
    if status == 'SKIP':
        raise _SkipExecution(message + ' was skipped.')
    assert status == 'FAIL', message + ' has status ' + repr(status) + '.'
    raise _SkipExecution(message + ' failed.')


def depends_on_test(name):
    _depends_on(_test_status_map, 'test case', name)


def depends_on_suite(name, status='PASS'):
    _depends_on(_suite_status_map, 'test suite', name)
