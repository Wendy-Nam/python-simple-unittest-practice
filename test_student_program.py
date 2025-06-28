import unittest
from unittest.mock import patch
from io import StringIO
import time
import student_program
from rich.console import Console
from rich.table import Table
from rich import box
from rich.text import Text
import pandas as pd

# Test metadata definition
TEST_CASES = [
    # 1. Register student then search: Register a student and immediately search to verify information is displayed correctly
    {
        "num": 1,
        "purpose": "Register student then search",
        "inputs": ["1", "John", "20", "95", "3", "John", "5"],
        "expected_output": ["Student John has been registered.", "Student John - Age: 20, Score: 95.0"]
    },
    # 2. Duplicate student registration: Check if duplicate registration warning is displayed when registering with an existing name
    {
        "num": 2,
        "purpose": "Duplicate student registration",
        "inputs": ["1", "John", "20", "95", "1", "John", "5"],
        "expected_output": ["Student John is already registered."]
    },
    # 3. Calculate average score: Register two students and verify average score is calculated and displayed correctly
    {
        "num": 3,
        "purpose": "Calculate average score",
        "inputs": ["1", "A", "20", "80", "1", "B", "21", "100", "4", "5"],
        "expected_output": ["The average score of all students is 90.00."]
    },
    # 4. Search non-existent student: Check if warning message is displayed when searching for a non-existent name
    {
        "num": 4,
        "purpose": "Search non-existent student",
        "inputs": ["3", "NonExistent", "5"],
        "expected_output": ["Student NonExistent not found."]
    },
    # 5. Print all students when no students exist: Check warning message when printing student list with no students
    {
        "num": 5,
        "purpose": "Print all students when no students exist",
        "inputs": ["2", "5"],
        "expected_output": ["No students are registered."]
    },
    # 6. Invalid menu input: Check warning message when entering a menu number that doesn't exist
    {
        "num": 6,
        "purpose": "Invalid menu input",
        "inputs": ["0", "5"],
        "expected_output": ["Invalid input."]
    },
    # 7. Register multiple students then print all
    {
        "num": 7,
        "purpose": "Register multiple students then print all",
        "inputs": ["1", "Tom", "19", "88", "1", "Jane", "21", "92", "2", "5"],
        "expected_output": [
            "Student Tom has been registered.",
            "Student Jane has been registered.",
            "Name: Tom, Age: 19, Score: 88.0",
            "Name: Jane, Age: 21, Score: 92.0"
        ]
    },
    # 8. Enter decimal score when registering student
    {
        "num": 8,
        "purpose": "Enter decimal score",
        "inputs": ["1", "Mike", "22", "87.5", "3", "Mike", "5"],
        "expected_output": [
            "Student Mike has been registered.",
            "Student Mike - Age: 22, Score: 87.5"
        ]
    },
    # 9. Enter negative age when registering student (no exception handling, registers normally)
    {
        "num": 9,
        "purpose": "Enter negative age",
        "inputs": ["1", "Jin", "-1", "70", "3", "Jin", "5"],
        "expected_output": [
            "Student Jin has been registered.",
            "Student Jin - Age: -1, Score: 70.0"
        ]
    },
    # 10. Check decimal places in average score after student registration
    {
        "num": 10,
        "purpose": "Check decimal places in average score",
        "inputs": ["1", "A", "20", "80.5", "1", "B", "21", "99.5", "4", "5"],
        "expected_output": [
            "The average score of all students is 90.00."
        ]
    },
    # 11. Calculate average score without registering students
    {
        "num": 11,
        "purpose": "Calculate average without students",
        "inputs": ["4", "5"],
        "expected_output": [
            "No students registered. Cannot calculate average score."
        ]
    },
    # 12. Search for specific student without registering students
    {
        "num": 12,
        "purpose": "Search without students",
        "inputs": ["3", "Anyone", "5"],
        "expected_output": [
            "Student Anyone not found."
        ]
    },
    # 13. Print all students without registering students
    {
        "num": 13,
        "purpose": "Print all without students",
        "inputs": ["2", "5"],
        "expected_output": [
            "No students are registered."
        ]
    },
    # 14. Program exit function
    {
        "num": 14,
        "purpose": "Program exit",
        "inputs": ["5"],
        "expected_output": []
    },
]


class TestStudentProgram(unittest.TestCase):

    def run_main_with_inputs(self, inputs):
        with patch('builtins.input', side_effect=inputs), \
             patch('sys.stdout', new_callable=StringIO) as fake_out:
            try:
                student_program.students.clear()
                student_program.main()
            except SystemExit:
                pass
            return fake_out.getvalue()

    def test_cases(self):
        results = []
        failed_outputs = []
        for case in TEST_CASES:
            start = time.time()
            output = self.run_main_with_inputs(case["inputs"])
            elapsed = time.time() - start
            is_success = all(exp in output for exp in case["expected_output"])
            results.append({
                "No.": case['num'],
                "Purpose": case["purpose"],
                "Input": "\n".join(case["inputs"]),
                "Expected": "\n".join(case["expected_output"]),
                "Result": "✅" if is_success else "❌",
                "Time": f"{elapsed:.3f}s",
                "Actual": output.strip()
            })
            if not is_success:
                failed_outputs.append(
                    f"[{case['num']}] {case['purpose']} - Actual output: {output.strip()}"
                )

        # rich table output (excluding actual output)
        console = Console()
        table = Table(
            title="🧪 Test Results Summary",
            box=box.ROUNDED,
            show_lines=True,
            padding=(0,1),
            expand=False
        )
        table.add_column("No.", style="bold cyan", width=4)
        table.add_column("Purpose", style="bold", width=10)
        table.add_column("Input", style="dim", width=12)
        table.add_column("Expected", style="green", width=14)
        table.add_column("Result", style="bold", width=4)
        table.add_column("Time", style="magenta", width=8)

        for row in results:
            table.add_row(
                str(row["No."]),
                row["Purpose"],
                Text(row["Input"], style="dim", overflow="ellipsis"),
                Text(row["Expected"], style="green", overflow="ellipsis"),
                row["Result"],
                row["Time"]
            )
        console.print("\n[bold underline]🧪 Test Results Summary[/]\n", style="bold magenta")
        console.print(table, justify="left")

        # Output actual output for failed cases
        if failed_outputs:
            console.print("\n[red]❌ Actual output for failed tests:[/]")
            for line in failed_outputs:
                console.print(line)

        # Save all results to Excel
        df = pd.DataFrame(results)
        df.to_excel("test_results.xlsx", index=False)

        self.assertTrue(all(r["Result"] == "✅" for r in results))

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=0)
