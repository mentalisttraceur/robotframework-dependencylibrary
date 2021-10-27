Robot Framework Dependency Library
==================================

Declare dependencies between tests.

Ideally tests are independent, but when tests depend
on earlier tests, DependencyLibrary makes it easy to
explicitly declare these dependencies and have tests
that depend on each other do the right thing.


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


Skipped Dependencies
--------------------

If a dependency was skipped, the depending test is also skipped:

.. code:: robotframework

    Skipped Test
        Skip  This test is skipped for some reason.

    A Test that Depends on "Skipped Test"
        Depends on test  Skipped Test
        Log  The rest of the keywords (including this log) will NOT run!

The skip message follows this format::

    Dependency not met: test case 'Skipped Test' status is 'SKIP'.


Failing Dependencies
--------------------

If a dependency failed, the depending test also fails:

.. code:: robotframework

    Failing Test
        Fail  This test failed for some reason.

    A Test that Depends on "Failing Test"
        Depends on test  Failing Test
        Log  The rest of the keywords (including this log) will NOT run!

The failure message follows this format::

    Dependency not met: test case 'Failing Test' status is 'FAIL'.


Other Failures
--------------

If you depend on a test or suite that does not exist or has not run yet,

.. code:: robotframework

    *** Test cases ***
    A Test that Depends on Missing Test Case
        Depends on test  Another Test

the test will fail and the failure message follows this format::

    Dependency not met: test case 'Another Test' not found.

If you make a test depend on itself or on the suite that contains it,

.. code:: robotframework

    *** Test cases ***
    Depends on self
        Depends on test  Depends on self

the test will fail and the failure message follows this format::

    Dependency not met: test case 'Depends on self' mid-execution.
