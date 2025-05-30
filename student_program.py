# 학생 정보를 저장할 딕셔너리 생성
students = {}

def register_student():
    # 입력 받을 항목과 자료형을 튜플로 정의
    prompts = [("이름", str), ("나이", int), ("점수", float)]
    info = {}

    # 각 항목별로 입력 받기
    for label, caster in prompts:
        value = input(f"학생 {label}을 입력하세요: ")
        # 이미 등록된 이름인지 확인
        if label == "이름" and value in students:
            print(f"{value} 학생은 이미 등록되어 있습니다.\n")
            return
        # 입력값을 지정한 자료형으로 변환하여 저장
        info[label] = caster(value)

    # 학생 정보를 딕셔너리에 저장
    students[info["이름"]] = {"나이": info["나이"], "점수": info["점수"]}
    print(f"{info['이름']} 학생이 등록되었습니다.\n")

def print_all_students():
    # 학생이 한 명도 없을 때 처리
    if not students:
        print("등록된 학생이 없습니다.\n")
        return
    print("전체 학생 목록:")
    # 모든 학생의 이름, 나이, 점수 출력
    for name, info in students.items():
        print(f"이름: {name}, 나이: {info['나이']}, 점수: {info['점수']}")
    print()

def search_student():
    # 검색할 학생 이름 입력 받기
    name = input("검색할 학생의 이름을 입력하세요: ")
    # 딕셔너리의 get()을 사용하면 없는 이름도 에러 없이 처리 가능
    info = students.get(name)
    if info:
        print(f"{name} 학생의 나이: {info['나이']}, 점수: {info['점수']}\n")
    else:
        print(f"{name} 학생을 찾을 수 없습니다.\n")

def calculate_average_score():
    # 학생이 없을 때 예외 처리
    if not students:
        print("학생이 없어 평균 점수를 계산할 수 없습니다.\n")
        return
    # 모든 학생의 점수 합을 구하고 학생 수로 나눔
    avg = sum(s["점수"] for s in students.values()) / len(students)
    print(f"전체 학생의 평균 점수는 {avg:.2f}점입니다.\n")

def main():
    # 메뉴 번호와 기능을 딕셔너리로 정의
    menu = {
        "1": ("학생 등록", register_student),
        "2": ("전체 학생 목록 출력", print_all_students),
        "3": ("특정 학생 검색", search_student),
        "4": ("평균 점수 출력", calculate_average_score),
        "5": ("프로그램 종료", exit)
    }

    while True:
        print("학생 정보 관리 프로그램")
        # 메뉴 출력
        for key, (desc, _) in menu.items():
            print(f"{key}. {desc}")
        # 사용자로부터 메뉴 번호 입력 받기
        choice = input("원하는 기능의 번호를 입력하세요: ")
        action = menu.get(choice)
        if action:
            # 선택한 기능 실행
            action[1]()
        else:
            # 잘못된 입력 처리
            print("잘못된 입력입니다. 다시 시도하세요.\n")

# 프로그램의 시작점
if __name__ == "__main__":
    main()