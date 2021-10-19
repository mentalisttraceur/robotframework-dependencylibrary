Robot Framework Dependency Library
==================================

Declare dependencies between tests. Make tests automatically
fail based on the results of other test cases or test suites.

Although I strongly recommend that people write tests to be independent,
sometimes, dependencies between tests are the simplest and easiest model
to implement, and having tests fail-fast if one or more previous test
cases didn't get the expected result can be beneficial.


Versioning
----------

This library's version numbers follow the `SemVer 2.0.0
specification <https://semver.org/spec/v2.0.0.html>`_.


Installation
------------

::

    pip install robotframework-dependencylibrary


Usage
-----

First, include the library in your tests:

.. code:: robotframework

    *** Settings ***
    Library  DependencyLibrary

Typical usage:

.. code:: robotframework

    *** Test cases ***
    Passing Test
        No operation

    A Test that Depends on "Passing Test"
        Depends on test  Passing Test
        Log  The rest of the keywords in this test will run as normal.

When you need to declare multiple dependencies, just repeat the keyword:

.. code:: robotframework


    *** Test cases ***
    Another Passing Test
        No operation

    A Test that Depends on Both "Passing Test" and "Another Passing Test"
        Depends on test  Passing Test
        Depends on test  Another Passing Test
        Log  The rest of the keywords in this test will run as normal.

You can also depend on the statuses of entire test suites:

.. code:: robotframework

    *** Test cases ***
    A Test that Depends on an Entire Test Suite Passing
        Depends on suite  Some Test Suite Name
        Log  The rest of the keywords in this test will run as normal.


Failures
--------

The ``Depends on ...`` keywords fail if the dependency is not
met, so the test case automatically aborts with a failure
unless you use something like ``Run keyword and expect error``.


Error Messages
--------------

The error messages are considered part of the interface,
so per `SemVer` the major version number will be bumped
if the error message format ever changes).

If a test failed when you expected it to pass,

.. code:: robotframework

    *** Test cases ***
    A Test that Depends on "Some Test" Passing
        Depends on test  Some Test
        Log  The rest of the keywords (including this log) will NOT run!

the error message will be::

    Dependency not met: test case 'Some Test' state is 'FAIL', wanted 'PASS'

If `Some Test` was skipped, the error message would be be::

    Dependency not met: test case 'Some Test' state is 'SKIP', wanted 'PASS'

If you typo a test, or try to depend on the status of a test
before it has been run, there won't be any status yet,

.. code:: robotframework

    *** Test cases ***
    A Test that Depends on Missing Test Case
        Depends on test  Another Test

so the error message will be::

    Dependency not met: test case 'Another Test' not found, wanted 'PASS'

If you accidentally make a test depend on itself,

.. code:: robotframework

    *** Test cases ***
    Depends on self
        Depends on test  Depends on self

the error message will be::

    Dependency not met: test case 'Depends on self' mid-execution, wanted 'PASS'

When depending on test suites, the error messages are the same,
but they use the words "test suite" instead of "test case".

.. note::

    If you need to programmatically parse the error messages, keep in
    mind that test case and suite names and statuses are quoted using
    logic equivalent to the Python built-in function ``repr``.


Extras
------

You'll probably never need to, but you can depend on a
failure or skip of a test or suite instead of success:

.. code:: robotframework

    *** Test cases ***
    Failing Test
        Fail  This test always fails

    A Test that Depends on "Failing Test" Failing
        Depends on test failure  Failing Test
        Log  The rest of the keywords in this test will run as normal.

    Skipped Test
        Skip  This test always skips

    A Test that Depends on "Skipped Test" Getting Skipped
        Depends on test skipped  Skipped Test
        Log  The rest of the keywords in this test will run as normal.

    A Test that Depends on an Entire Test Suite Failing
        Depends on suite falure  Another Test Suite Name
        Log  The rest of the keywords in this test will run as normal.

    A Test that Depends on an Entire Test Suite Getting Skipped
        Depends on suite skipped  Some Test Suite Name
        Log  The rest of the keywords in this test will run as normal.

For symmetry with the above, the keywords ``Depends on test success``
and ``Depends on suite success`` are available as synonyms for
``Depends on test`` and ``Depends on suite``.

.. code:: robotframework

    *** Test cases ***
    This Test Depends on "Passing Test" Passing (using alternate keyword)
        Depends on test success  Passing Test
        Log  The rest of the keywords in this test will run as normal.
