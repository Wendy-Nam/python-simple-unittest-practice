#!/bin/bash

echo "🧪 학생 정보 관리 프로그램 자동 테스트 시작"
echo "=============================="

if [ -f requirements.txt ]; then
  echo "🔍 requirements.txt 발견, 필요한 패키지 설치 시도..."
  pip3 install -r requirements.txt
  if [ $? -ne 0 ]; then
    echo "❌ requirements.txt 기반 패키지 설치 실패! pip 환경을 확인하세요."
    exit 1
  fi
else
  REQUIRED_PKGS=("tabulate" "rich" "pandas")
  for pkg in "${REQUIRED_PKGS[@]}"; do
    python3 -c "import $pkg" 2>/dev/null
    if [ $? -ne 0 ]; then
      echo "🔧 $pkg 패키지가 없어 자동 설치합니다..."
      pip3 install $pkg
      if [ $? -ne 0 ]; then
        echo "❌ $pkg 설치 실패! pip 환경을 확인하세요."
        exit 1
      fi
    fi
  done
fi

python3 test_student_program.py
if [ $? -eq 0 ]; then
  echo "✅ 모든 테스트 성공!"
else
  echo "❌ 테스트 실패! 코드를 다시 확인하세요."
fi
echo "=============================="