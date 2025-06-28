# Python unittest Automation Testing Example

> Automated testing practice for simple Python example code. Summarize results with rich & pandas, export to Excel.

This is a practice project for applying automated input/output testing to simple Python example code.

**This is an example created to learn practice/example/automated testing structure.**

## Overview

- **Functional code** provides features to register student name, age, and score, print all students, search specific students, calculate average scores, and exit the program.
- **Test program** performs input automation, continuous testing, and result comparison based on **test cases** defined at the top.
- This is an example repository for practicing basic Python implementation and test automation.
- Uses [rich](https://github.com/Textualize/rich), [pandas](https://pandas.pydata.org/), [tabulate](https://pypi.org/project/tabulate/), and [openpyxl](https://openpyxl.readthedocs.io/) packages for test automation and result summary output.

## File Structure

- `student_program.py` : Example student information management code (test target)
- `test_student_program.py` : unittest-based automated testing and result summary
- `requirements.txt` : List of required packages
- `run_test.sh` : Automated test execution script

## How to Run

1. Install packages  
   (Virtual environment recommended)
   ```sh
   pip install -r requirements.txt
   ```

2. Run program directly  
   ```sh
   python student_program.py
   ```

3. Run automated tests  
   ```sh
   bash run_test.sh
   ```
   - Checks if required packages are installed, then runs the unit test `test_student_program.py`.
   - Test results are displayed as a rich table and saved to `test_results.xlsx` file.

## Notes

- Test cases include various input scenarios (normal/exception/edge cases, etc.).
- You can freely modify/extend the code and test structure for reference.
