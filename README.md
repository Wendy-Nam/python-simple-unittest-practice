# 자동화 테스트 예제 - 파이썬 unittest

> 간단한 파이썬 예제 코드의 자동화 테스트 실습. rich와 pandas로 결과 요약 및 엑셀 저장.

> Automated testing practice for simple Python code. Summarize results with rich & pandas, export to Excel.

- 간단한 파이썬 예제 코드에 대해 자동화된 입력/출력 테스트를 적용하는 실습입니다.

- **실습/예제/자동화 테스트 구조를 익히기 위해 만든 예시입니다.**

## 소개

- **기능적 코드**는 학생의 이름, 나이, 점수를 등록하고, 전체 목록 출력, 특정 학생 검색, 평균 점수 계산, 프로그램 종료 기능을 제공합니다.
- **테스트 프로그램**은 상단에 정의된 **테스트 케이스**를 토대로 입력 자동화, 연속 테스트, 결과 비교 등을 수행합니다. 
- Python 기본 구현과 테스트 자동화 연습을 위한 예제 레포지토리입니다.
- 테스트 자동화 및 결과 요약 출력을 위해 [rich](https://github.com/Textualize/rich), [pandas](https://pandas.pydata.org/), [tabulate](https://pypi.org/project/tabulate/) 패키지를 사용합니다.

## 파일 구성

- `student_program.py` : 예제용 학생 정보 관리 코드 (테스트 대상)
- `test_student_program.py` : unittest 기반 자동화 테스트 및 결과 요약
- `requirements.txt` : 필요한 패키지 목록
- `run_test.sh` : 테스트 자동 실행 스크립트

## 실행 방법

1. 패키지 설치  
   (가상환경 권장, 필요시)
   ```sh
   pip install -r requirements.txt
   ```

2. 프로그램 직접 실행  
   ```sh
   python student_program.py
   ```

3. 테스트 자동 실행  
   ```sh
   bash run_test.sh
   ```
   - 필요한 패키지 설치 여부를 확인한 뒤, 유닛테스트인 `test_student_program.py`를 실행합니다.
   - 테스트 결과가 rich 테이블로 출력되고, `test_results.xlsx` 파일로 저장됩니다.

## 참고

- 테스트 케이스는 다양한 입력 상황(정상/예외/엣지케이스 등)을 포함합니다.
- 코드와 테스트 구조를 참고하여 자유롭게 수정/확장할 수 있습니다.