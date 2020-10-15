*** Settings ***
Library  DependencyLibrary

*** Test cases ***
Passing Test
    No operation

Failing Test
    Fail  This test is intentionally hardcoded to fail

Depends on Non-Existant Test Case
    #Run keyword and expect error
    #...  Dependency not met: test case 'Misnamed Test' not found, wanted 'PASS'
    #...  Depends on test  Misnamed Test
    Depends on test  Misnamed Test

Depends on self
    #Run keyword and expect error
    #...  Dependency not met: test case 'Depends on self'*
    #...  Depends on test  Depends on self
    Depends on test  Depends on self

Depends on self-suite
    #Run keyword and expect error
    #...  Dependency not met: test suite 'test' not found, wanted 'PASS'
    #...  Depends on suite  test
    Depends on suite  test

Depends on Passing Test Passing
    Depends on test  Passing Test

Depends on Passing Test Failing
    #Run keyword and expect error
    #...  Dependency not met: test case 'Passing Test' state is 'PASS', wanted 'FAIL'
    #...  Depends on test failure  Passing Test
    Depends on test failure  Passing Test

Depends on Failing Test Passing
    #Run keyword and expect error
    #...  Dependency not met: test case 'Failing Test' state is 'FAIL', wanted 'PASS'
    #...  Depends on test  Failing Test
    Depends on test  Failing Test

Depends on Failing Test Failing
    Depends on test failure  Failing Test
