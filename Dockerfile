FROM python:3.9-slim

# 작업 디렉터리 설정
WORKDIR /app

# 필요한 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# uvicorn 실행 (main.py 안에 app 이라는 FastAPI 인스턴스가 있다고 가정)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
