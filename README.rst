Robot Framework Dependency Library
==================================

Declare dependencies between tests. Make tests automatically fail based
on the results of other test cases or test suites.

Although I strongly recommend that people write tests to be independent,
sometimes, dependencies between tests are the simplest and easiest model
to implement, and having tests fail-fast if one or more previous test
cases didn't get the expected result can be beneficial.


Usage
-----

First, include the library in your tests (if you copied/cloned the
DependencyLibrary.py from the repository, make sure the directory
containing it is passed to ``robot`` with the ``--pythonpath`` option):

.. code:: robotframework

    *** Settings ***
    Library  DependencyLibrary

Let's say you have a passing and failing test:

.. code:: robotframework

    *** Test cases ***
    Passing Test
        No operation

    Failing Test
        Fail  This test is intentionally hardcoded to fail

A basic test that depends on the passing test looks like this:

.. code:: robotframework

    *** Test cases ***
    This Test Depends on "Passing Test" Passing
        Depends on test  Passing Test
        Log  The rest of the keywords in this test will run as normal.

Of course, you can depend on a test failure instead:

.. code:: robotframework

    *** Test cases ***
    This Test Depends on "Failing Test" Failing
        Depends on test failure  Failing Test
        Log  The rest of the keywords in this test will run as normal.

You can also depend on the status of a test suite:

.. code:: robotframework

    *** Test cases ***
    Depends on test suite
        Depends on suite  My Test Suite Name
        Log  The rest of the keywords in this test will run as normal.


Failures
--------

Since the ``Depends on ...`` keywords fail when the dependency is not
met, it supports all the usual logic you'd expect from Robot Framework:

The test case automatically aborts with a failure when the ``Depends on
...`` keyword fails as you'd expect, unless you capture the status and
error message using something like ``Run keyword and expect error``.


Error Messages
--------------

The error messages are documented (and are considered part of the
interface, so you can rely on `SemVer` semantics: the major version
number will be bumped if the logic for error messages ever changes):

If a test failed when you expected it to pass, you'll get a helpful error:

.. code:: robotframework

    *** Test cases ***
    This Test Depends on "Failing Test" Passing
        Depends on test  Failing Test
        Log  The rest of the keywords (including this log) will NOT run!

The error message will be::

    Dependency not met: test case 'Failing Test' state is 'FAIL', wanted 'PASS'

Same with expecting a passing test to fail:

.. code:: robotframework

    *** Test cases ***
    This Test Depends on "Passing Test" Failing
        Depends on test failure  Passing Test
        Log  The rest of the keywords (including this log) will NOT run!

The error message will be::

    Dependency not met: test case 'Passing Test' state is 'PASS', wanted 'FAIL'

If you typo a test, or try to depend on the status of the test before
it's been run, for example:

.. code:: robotframework

    *** Test cases ***
    Depends on Non-Existant Test Case
        Depends on test  Misnamed Test

The error message will be::

    Dependency not met: test case 'Misnamed Test' not found, wanted 'PASS'

If you accidentally make a test depend on itself, it will give a similar
error message that more precisely identifies the error:

.. code:: robotframework

    *** Test cases ***
    Depends on self
        Depends on test  Depends on self

The error message will be::

    Dependency not met: test case 'Depends on self' mid-execution, wanted 'PASS'

All test suite error messages are the same, except that they use the
words "test suite" instead of "test case".

.. note::

    If you need to programmatically parse the error messages, keep in
    mind that test case and suite names and statuses are quoted using
    logic equivalent to the Python built-in function ``repr``.


Extras
------

For symmetry with ``Depends on test failure``, the keyword ``Depends on
test success`` is available as a synonym for ``Depends on test``:

.. code:: robotframework

    *** Test cases ***
    This Test Depends on "Passing Test" Passing (using alternate keyword)
        Depends on test success  Passing Test
        Log  The rest of the keywords in this test will run as normal.
