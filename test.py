"""A test harness for the CS259 PLM language."""

from dataclasses import dataclass
from pathlib import Path
from subprocess import TimeoutExpired, run
from re import compile as re_compile
from time import perf_counter
from typing import Optional


# Constant configuration variables
PROGRAM_FILE: str = "Assignment.jj"
OUTPUT_EXECUTABLE: str = "Assignment"
TESTS_DIRECTORY: str = "tests"
TEST_TIMEOUT: float = 5.0
SHOW_FAILURE: bool = True
STDTYPE_DELIMITER: str = "=====\n"
WRITE_OUTPUT: bool = False


# Set terminal string colour escape codes
OKGREEN = "\033[92m"
OKBLUE = "\033[94m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"


@dataclass
class Tester:
    """A class to run the tests."""

    tests_run: int = 0
    tests_passed: int = 0
    tests_failed: int = 0
    tests_timedout: int = 0
    time_taken: float = 0
    num_tests: Optional[int] = None

    def compile(self):
        """Compile the JavaCC code"""
        print(f"{OKBLUE}===== Compiling JavaCC code ====={ENDC}")
        run(["javacc", PROGRAM_FILE], check=False)
        run(["javac *.java"], shell=True, check=False)
        print(f"{OKBLUE}===== Compiled JavaCC code ====={ENDC}\n\n")

    def test(self):
        """Run the tests on the compiled JavaCC code.

        Test cases should be given as .txt files including the word "test" in
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
        """
        try:
            tests_dir = Path(TESTS_DIRECTORY)
            test_pattern = re_compile(r".*test.*\.txt")
            test_files: list[str] = []

            for file in tests_dir.rglob("*"):
                if test_pattern.match(file.name):
                    test_files.append(str(file.resolve()))

            self.num_tests = len(test_files)

            print(f"{OKBLUE}===== Starting tests ====={ENDC}")

            if WRITE_OUTPUT:
                print("Writing output to test files. Proceed [y/N]? ", end="")
                if input().lower() not in ["y", "yes"]:
                    exit(0)

            for test_file in test_files:
                print(f"{OKBLUE}{self.tests_run+1}/{self.num_tests}){ENDC}", end="")
                self.tests_run += 1

                single_time = 0.0
                try:
                    with open(test_file, "r", encoding="utf-8") as file_handle:
                        file_data = file_handle.read().split(STDTYPE_DELIMITER)
                        test_case = file_data[0]
                        expected_result = STDTYPE_DELIMITER.join(file_data[1:])
                    single_time = perf_counter()
                    result = run(
                        ["java", OUTPUT_EXECUTABLE],
                        capture_output=True,
                        timeout=TEST_TIMEOUT,
                        input=test_case.encode("utf-8"),
                        check=False,
                    )
                    single_time = perf_counter() - single_time
                    self.time_taken += single_time
                    output = result.stdout.decode("utf-8")
                    error = result.stderr.decode("utf-8")
                    if "JAVA" in error.upper():
                        error = "\n".join(error.split("\n")[1:])
                    actual_result = f"{output}=====\n{error}"
                except TimeoutExpired:
                    print(
                        f"\tTest {test_file} {WARNING}timed out{ENDC} in {single_time:.3f}s"
                    )
                    self.tests_timedout += 1
                    continue

                # Check if the results are correct
                if actual_result == expected_result:
                    print(
                        f"\tTest {test_file.split('/')[-1]} is "
                        f"{OKGREEN}correct{ENDC} in {single_time:.3f}s"
                    )
                    self.tests_passed += 1
                else:
                    print(
                        f"\tTest {test_file.split('/')[-1]} is "
                        f"{FAIL}wrong{ENDC} in {single_time:.3f}s"
                    )
                    if SHOW_FAILURE:
                        print(f"\n{WARNING}Expected:{ENDC}\n{expected_result}")
                        print(f"{WARNING}Got:{ENDC}\n{actual_result}", end="")
                    self.tests_failed += 1

                # If enabled write outputs to empty test files
                if WRITE_OUTPUT and expected_result == "":
                    with open(test_file, "a", encoding="utf-8") as file_handle:
                        file_handle.write(actual_result)

            print(f"{OKBLUE}===== Finished tests ====={ENDC}")

        except KeyboardInterrupt:
            # Fail gracefully on keyboard interrupt
            print(f"\t{FAIL}Keyboard interrupt{ENDC}")

    def __repr__(self):
        """Return a string representation of the test object."""
        print()
        if self.tests_run == 0:
            return "No tests run yet"
        return f"{self.tests_passed}/{self.num_tests} tests passed in {self.time_taken:.3f}s"


if __name__ == "__main__":
    # Initialise, run, and cleanup the tester
    tester = Tester()
    tester.compile()
    tester.test()
    print(tester)
