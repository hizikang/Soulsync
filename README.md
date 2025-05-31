# SoulSync

## 1. 프로젝트 개요

### 한 줄 요약

> 사용자의 감정을 배우어 그 기분에 맞는 음악과 위로 메시지를 추천하는 AI 기반 맞추리 음악 서비스

### 해결하고자 한 문제

* 기존 음악 추천 서비스는 주로 사용자의 청취 이력이나 선호 장르에 초점을 맞추고 있어, 사용자의 **현재 감정**을 반영하지 못함
* SoulSync는 사용자가 자신의 감정을 이미지 또는 텍스트 입력을 통해 표현하면, AI 모델이 이를 분석하여 해당 감정에 어울리는 음악과 공감 메시지를 제공함으로써, 보다 개인화된 경험을 제공함

### 주요 기능

* 감정 분석: KoBERT 기반 해당 AI 모델을 통해 텍스트 기반 감정 분석
* 맞추 음악 추천: CSV 데이터에서 감정과 맞는 건을 찾아서 추천
* 공감 메시지 제공: 감정에 맞는 위로가 포함된 메시지와 함께 보조

---

## 2. 파일 구조

```
SOULSYNC/
├─ crawling/                 음악 크롤링
├─ data/                     데이터 파일
├─ models/                   감정 분석 모델 로드
├─ static/                   CSS, JS
├─ templates/                HTML
├─ utils/                    로그인/회원가입, 노래 추천
├─ main.py                   main.py
├─ requirements.txt          필요 패키지 목록
└─ README.md
```

---

## 3. 기술 스택

* **Backend**: FastAPI, Python
* **AI**: Hugging Face Transformers (KoBERT)
* **DB**: SQLite
* **Frontend**: HTML, CSS, JS, Jinja2
* **Server**: Uvicorn

---

## 4. 설치 및 실행 방법

```bash
# 클론
$ git clone https://github.com/hzzz15/Soulsync.git
$ cd Soulsync

# 개발 가상 환경
$ python -m venv venv
$ source venv/bin/activate  # Windows: venv\Scripts\activate

# 필요 패키지 설치
$ pip install -r requirements.txt

# KoBERT tokenizer 설치
# 모델은 Hugging Face에서 불러오지만, tokenizer는 로컬에서 불러오기 때문에 아래 명령을 반드시 실행해야 합니다.
$ transformers-cli download skt/kobert-base-v1
# 또는 transformers 4.30 이상일 경우
$ from transformers import BertTokenizer; BertTokenizer.from_pretrained("skt/kobert-base-v1")

# 실행
$ uvicorn main:app --reload
```

* 사용: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Swagger 문서: /docs

---

## 5. 시연 경로

* 회원가입 / 로그인
![회원가입-로그인](assets/1.gif)
* 박스 선택 노래 추천
![박스 선택 노래 추천](assets/2.gif)
* 감정 입력 노래 추천
![감정 입력 노래 추천](assets/3.gif)

---

## 7. 팀원 소개

- 강희지: AI / Backend / Frontend
- 송종욱: DB
- 신효진: Frontend / Design
- 지은혜: Frontend / Crawling
- 권승빈: Frontend
- 박성빈: Frontend

> SoulSync는 사용자의 감정을 기반으로 한 차별화된 음악 추천 서비스를 제공합니다.
