# PLM Test Harness

## About

The CS259 coursework spec provides a set of simple examples
and non-examples for testing your implementation of the PLM
(Programming Language of the Moment) parser and interpreter.
Additionally, in previous years
[students wrote an extended set of tests along with a simple bash script to run them](https://github.com/Department-of-Administrative-Affairs/CS259-tests).

I wrote an improved version of this test harness in Python,
with many additional tests for edge cases when I was completing
the coursework in 2021.

## What is tested?

- In the `specification/` folder, the examples and non-examples from the specification
- In the `department_admin_affairs/` folder, the [test cases from the "Department of Administrative Affairs" student repository](https://github.com/Department-of-Administrative-Affairs/CS259-tests/tree/master/testprograms). *Note that these tests should be modified to include your custom error messages*
- In the `_accept/` folder, a set of tests to exercise syntactic and semantic edge cases which should pass
- In the `_reject/` folder, a set of tests to exercise syntactic edge cases which should fail. *Note that these tests should be modified to include your custom error messages*

## Usage

First, copy the `test.py` file and the `tests/` directory to the directory
containing your `Assignment.jj` file.

Then, the test harness can be run as (requires python versions >= 3.7):

```bash
python3.11 test.py
```

This should run all the tests and print a colour-coded output for which
ones passed and failed.

### Why do I need to add my own error messages for failing tests?

Part of the assessment for this coursework is error handling. As a result
of this, I have redacted all my error messages for the failing tests, as
they would allude to my approach to error handling, and my approach
shouldn't be treated as a canonical solution anyway.

***As a result of this, for failing tests you should edit the test files
to add the line number and error message of the failure.***

### Test file format

Test cases should be given as text files including the word "test" in
their name. The schema of the file is the stdin, followed by the stdout,
followed by the stderr, seperated by `=====\n` (5 equals on a newline).

For example, the first test case in the specification would be:

```test
DEF MAIN { 1+ADDFOUR(2+ADDFOUR(3)) } ;
DEF ADDFOUR x { x+4 } ;
=====
PASS
14
=====
```

Since the format is written in this way, you can add your own tests by creating
new text files in the `test/` directory which include the word test in their
name. They will then automatically get picked up and drive your JavaCC implementation.

*If you write additional tests, please consider pull requesting them into this
repository for others to use as well!*

## Other notes

At the time I wrote these tests, I checked with the module
organiser that it was acceptable to share them (with the
modification of not sharing error messages), as they are not
coursework solutions, just a set of helpful tests. If I am
ever told that this policy has changed, I will make this
repository private.

Note that the coursework spec is subject to change, so it
is possible that some tests will become out of date. This
is a non-official set of tests made by a fallible student,
so do not rely on them as ground truth!

