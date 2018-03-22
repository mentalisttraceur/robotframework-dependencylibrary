# Copyright 2017 Alexander Kozhevnikov <mentalisttraceur@gmail.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


__version__ = '1.0.0'


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

    # "SKIP" state does not yet exist but is a target feature for
    # Robot Framework 3.1.
    #def depends_on_test_skipped(self, name):
    #    return self.depends_on_test(name, 'SKIP')

    def depends_on_suite(self, name):
        return self._depends_on_suite(name)

    def depends_on_suite_success(self, name):
        return self._depends_on_suite(name)

    def depends_on_suite_failure(self, name):
        return self._depends_on_suite(name, 'FAIL')

    # Not sure if "SKIP" state will apply to suites or just tests:
    #def depends_on_suite_skipped(self, name):
    #    return self.depends_on_suite(name, 'SKIP')
