# SPDX-License-Identifier: 0BSD
# Copyright 2017 Alexander Kozhevnikov <mentalisttraceur@gmail.com>


__version__ = '1.0.1'


def _depends_on(status_map, dependency_type, name, status):
    _status = status_map.get(name.lower(), None)
    assert _status is not None, (
        'Dependency not met: %s %r not found, wanted %r'
        % (dependency_type, name, status))
    assert _status is not Ellipsis, (
        'Dependency not met: %s %r mid-execution, wanted %r'
        % (dependency_type, name, status))
    assert _status == status, (
        'Dependency not met: %s %r state is %r, wanted %r'
        % (dependency_type, name, _status, status))


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

    def _depends_on_test(self, name, status='PASS'):
        _depends_on(self._test_status_map, 'test case', name, status)

    def _depends_on_suite(self, name, status='PASS'):
        _depends_on(self._suite_status_map, 'test suite', name, status)

    def depends_on_test(self, name):
        return self._depends_on_test(name)

    def depends_on_test_success(self, name):
        return self._depends_on_test(name)

    def depends_on_test_failure(self, name):
        return self._depends_on_test(name, 'FAIL')

    def depends_on_test_skipped(self, name):
        return self._depends_on_test(name, 'SKIP')

    def depends_on_suite(self, name):
        return self._depends_on_suite(name)

    def depends_on_suite_success(self, name):
        return self._depends_on_suite(name)

    def depends_on_suite_failure(self, name):
        return self._depends_on_suite(name, 'FAIL')

    def depends_on_suite_skipped(self, name):
        return self._depends_on_suite(name, 'SKIP')
