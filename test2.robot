*** Settings ***
Library  DependencyLibrary

*** Test cases ***
a
    No operation

b
    No operation

c
    Depends on test    a
    Depends on test    b
