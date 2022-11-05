# SPDX-License-Identifier: 0BSD
# Copyright 2017 Alexander Kozhevnikov <mentalisttraceur@gmail.com>

from robot.api import logger as _logger
from robot.api import SkipExecution as _SkipExecution


__all__ = ('DependencyLibrary',)
__version__ = '3.0.1'


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


class DependencyLibrary(object):
    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self._test_status_map = {}
        self._suite_status_map = {}

    def _start_test(self, test, result):
        self._test_status_map[test.name.lower()] = Ellipsis

    def _end_test(self, test, result):
        self._test_status_map[test.name.lower()] = result.status

    def _start_suite(self, suite, result):
        self._suite_status_map[suite.name.lower()] = Ellipsis

    def _end_suite(self, suite, result):
        self._suite_status_map[suite.name.lower()] = result.status

    def depends_on_test(self, name):
        _depends_on(self._test_status_map, 'test case', name)

    def depends_on_suite(self, name, status='PASS'):
        _depends_on(self._suite_status_map, 'test suite', name)
