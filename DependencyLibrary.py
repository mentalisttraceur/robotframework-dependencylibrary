# SPDX-License-Identifier: 0BSD
# Copyright 2017 Alexander Kozhevnikov <mentalisttraceur@gmail.com>

try:
    from robot.api import SkipExecution as _SkipExecution
except ImportError:
    pass


__all__ = ('DependencyLibrary',)
__version__ = '2.0.5'


def _depends_on(status_map, dependency_type, name):
    message = 'Dependency not met: ' + dependency_type + ' ' + repr(name)
    status = status_map.get(name.lower(), None)
    if status is None:
        raise AssertionError(message + ' not found.')
    if status is Ellipsis:
        raise AssertionError(message + ' mid-execution.')
    if status == 'PASS':
        return
    message = message + ' status is ' + repr(status) + '.'
    if status == 'SKIP':
        raise _SkipExecution(message)
    raise AssertionError(message)


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
