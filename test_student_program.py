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

# 테스트 메타데이터 정의
TEST_CASES = [
    # 1. 학생 등록 후 검색: 학생을 등록하고, 바로 검색해서 정보가 정확히 출력되는지 확인
    {
        "num": 1,
        "purpose": "학생 등록 후 검색",
        "inputs": ["1", "홍길동", "20", "95", "3", "홍길동", "5"],
        "expected_output": ["홍길동 학생이 등록되었습니다.", "홍길동 학생의 나이: 20, 점수: 95.0"]
    },
    # 2. 중복 학생 등록: 이미 등록된 이름으로 다시 등록 시 중복 안내가 출력되는지 확인
    {
        "num": 2,
        "purpose": "중복 학생 등록",
        "inputs": ["1", "홍길동", "20", "95", "1", "홍길동", "5"],
        "expected_output": ["홍길동 학생은 이미 등록되어 있습니다."]
    },
    # 3. 평균 점수 출력: 두 명 등록 후 평균 점수가 올바르게 계산되어 출력되는지 확인
    {
        "num": 3,
        "purpose": "평균 점수 출력",
        "inputs": ["1", "A", "20", "80", "1", "B", "21", "100", "4", "5"],
        "expected_output": ["전체 학생의 평균 점수는 90.00점입니다."]
    },
    # 4. 존재하지 않는 학생 검색: 없는 이름으로 검색 시 안내 메시지가 출력되는지 확인
    {
        "num": 4,
        "purpose": "존재하지 않는 학생 검색",
        "inputs": ["3", "없는학생", "5"],
        "expected_output": ["없는학생 학생을 찾을 수 없습니다."]
    },
    # 5. 학생 없는 상태에서 전체 목록 출력: 학생이 없을 때 목록 출력 시 안내 메시지 확인
    {
        "num": 5,
        "purpose": "학생 없는 상태에서 전체 목록 출력",
        "inputs": ["2", "5"],
        "expected_output": ["등록된 학생이 없습니다."]
    },
    # 6. 잘못된 메뉴 입력: 메뉴에 없는 번호 입력 시 안내 메시지 확인
    {
        "num": 6,
        "purpose": "잘못된 메뉴 입력",
        "inputs": ["0", "5"],
        "expected_output": ["잘못된 입력입니다."]
    },
    # 7. 학생 여러 명 등록 후 전체 목록 출력
    {
        "num": 7,
        "purpose": "여러 학생 등록 후 전체 목록 출력",
        "inputs": ["1", "철수", "19", "88", "1", "영희", "21", "92", "2", "5"],
        "expected_output": [
            "철수 학생이 등록되었습니다.",
            "영희 학생이 등록되었습니다.",
            "이름: 철수, 나이: 19, 점수: 88.0",
            "이름: 영희, 나이: 21, 점수: 92.0"
        ]
    },
    # 8. 학생 등록 시 점수에 소수 입력
    {
        "num": 8,
        "purpose": "점수에 소수 입력",
        "inputs": ["1", "민수", "22", "87.5", "3", "민수", "5"],
        "expected_output": [
            "민수 학생이 등록되었습니다.",
            "민수 학생의 나이: 22, 점수: 87.5"
        ]
    },
    # 9. 학생 등록 시 나이에 음수 입력 (예외처리 없음, 정상 등록됨)
    {
        "num": 9,
        "purpose": "나이에 음수 입력",
        "inputs": ["1", "진수", "-1", "70", "3", "진수", "5"],
        "expected_output": [
            "진수 학생이 등록되었습니다.",
            "진수 학생의 나이: -1, 점수: 70.0"
        ]
    },
    # 10. 학생 등록 후 평균 점수 소수점 확인
    {
        "num": 10,
        "purpose": "평균 점수 소수점 확인",
        "inputs": ["1", "A", "20", "80.5", "1", "B", "21", "99.5", "4", "5"],
        "expected_output": [
            "전체 학생의 평균 점수는 90.00점입니다."
        ]
    },
    # 11. 학생 등록 없이 평균 점수 출력
    {
        "num": 11,
        "purpose": "학생 없이 평균 점수 출력",
        "inputs": ["4", "5"],
        "expected_output": [
            "학생이 없어 평균 점수를 계산할 수 없습니다."
        ]
    },
    # 12. 학생 등록 없이 특정 학생 검색
    {
        "num": 12,
        "purpose": "학생 없이 검색",
        "inputs": ["3", "아무개", "5"],
        "expected_output": [
            "아무개 학생을 찾을 수 없습니다."
        ]
    },
    # 13. 학생 등록 없이 전체 목록 출력
    {
        "num": 13,
        "purpose": "학생 없이 전체 목록 출력",
        "inputs": ["2", "5"],
        "expected_output": [
            "등록된 학생이 없습니다."
        ]
    },
    # 14. 프로그램 종료 기능
    {
        "num": 14,
        "purpose": "프로그램 종료",
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
                "목적": case["purpose"],
                "입력": "\n".join(case["inputs"]),
                "예상결과": "\n".join(case["expected_output"]),
                "정답": "✅" if is_success else "❌",
                "실행시간": f"{elapsed:.3f}s",
                "실제출력": output.strip()
            })
            if not is_success:
                failed_outputs.append(
                    f"[{case['num']}] {case['purpose']} - 실제출력: {output.strip()}"
                )

        # rich 테이블 출력 (실제출력 제외)
        console = Console()
        table = Table(
            title="🧪 테스트 결과 요약",
            box=box.ROUNDED,
            show_lines=True,
            padding=(0,1),
            expand=False
        )
        table.add_column("No.", style="bold cyan", width=4)
        table.add_column("목적", style="bold", width=10)
        table.add_column("입력", style="dim", width=12)
        table.add_column("예상결과", style="green", width=14)
        table.add_column("정답", style="bold", width=4)
        table.add_column("실행시간", style="magenta", width=8)

        for row in results:
            table.add_row(
                str(row["No."]),
                row["목적"],
                Text(row["입력"], style="dim", overflow="ellipsis"),
                Text(row["예상결과"], style="green", overflow="ellipsis"),
                row["정답"],
                row["실행시간"]
            )
        console.print("\n[bold underline]🧪 테스트 결과 요약[/]\n", style="bold magenta")
        console.print(table, justify="left")

        # 실패한 케이스 실제출력 출력
        if failed_outputs:
            console.print("\n[red]❌ 실패한 테스트의 실제 출력:[/]")
            for line in failed_outputs:
                console.print(line)

        # 전체 결과를 엑셀로 저장
        df = pd.DataFrame(results)
        df.to_excel("test_results.xlsx", index=False)

        self.assertTrue(all(r["정답"] == "✅" for r in results))

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=0)
