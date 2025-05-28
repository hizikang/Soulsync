from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from utils.recommendation import analyze_text, MOOD_MAPPING, render_list_page, render_box_page, MOOD_COMMENTS
from fastapi.templating import Jinja2Templates
import pandas as pd
import random
import json

from utils.database import setup_database
from utils.auth import login_user, signup_user, logout_user
from utils.pages import (
    render_index, render_login, render_signup, render_home, render_welcome,
    render_forgot_password, render_main, render_sing, render_favicon
)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
songs_data = pd.read_csv("data/songs.csv")

setup_database()

# 페이지 렌더링
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return render_index(request)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return render_login(request)

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return render_signup(request)

@app.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    return render_home(request)

@app.get("/welcome", response_class=HTMLResponse)
async def welcome_page(request: Request):
    return render_welcome(request)

@app.get("/main", response_class=HTMLResponse)
async def main_page(request: Request):
    return render_main(request)

@app.get("/sing", response_class=HTMLResponse)
async def sing_page(request: Request):
    return render_sing(request)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return render_favicon()

# 인증 관련 라우트
@app.post("/login")
async def login_endpoint(request: Request, username: str = Form(...), password: str = Form(...)):
    return await login_user(request, username, password)

@app.post("/signup")
async def signup_endpoint(username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    return await signup_user(username, password, confirm_password)

@app.get("/logout")
def logout_endpoint(request: Request):
    return logout_user(request)

# 감정 텍스트 입력 노래 추천 관련 라우트
@app.post("/analyze")
async def analyze_endpoint(user_text: str = Form(...)):
    try:
        sentiment = analyze_text(user_text)
        return {"text": user_text, "sentiment": sentiment}
    except Exception as e:
        return {"error": f"오류 발생: {str(e)}"}

@app.post("/recommend", response_class=HTMLResponse)
async def recommend_entry(request: Request, user_text: str = Form(...)):
    try:
        # 감정 분석 결과
        sentiment = analyze_text(user_text)
        print(f"[DEBUG] 분석된 감정: {sentiment}")

        # 공백 제거 
        mood = sentiment.strip()

        # 해당 mood에 맞는 곡 필터링
        filtered_songs = songs_data[songs_data["Mood"] == mood].drop_duplicates(subset="Song")

        if filtered_songs.empty:
            return templates.TemplateResponse("recommend.html", {
                "request": request,
                "songs": [],
                "mood": mood,
                "feedback": f"'{mood}'에 맞는 추천곡을 찾을 수 없습니다."
            })

        # 최대 12곡 랜덤 추출
        recommended = filtered_songs.sample(n=min(12, len(filtered_songs))).to_dict(orient="records")

        # 감정 피드백 문장
        feedback = random.choice(MOOD_COMMENTS.get(mood, ["오늘의 추천입니다."]))

        return templates.TemplateResponse("recommend.html", {
            "request": request,
            "songs": recommended,
            "mood": mood,
            "feedback": feedback
        })
    except Exception as e:
        print(f"[ERROR] recommend 실패: {e}")
        return JSONResponse(content={"error": f"추천 실패: {str(e)}"}, status_code=500)

@app.post("/list", response_class=HTMLResponse)
async def list_from_mix(request: Request, mood: str = Form(...), songs_json: str = Form(...)):
    try:
        # 전달된 MIX 곡 4개
        mix_songs = json.loads(songs_json)
        mix_titles = {song["Song"] for song in mix_songs}

        # mood에서 mix에 없는 곡만
        additional_pool = songs_data[
            (songs_data["Mood"] == mood) & (~songs_data["Song"].isin(mix_titles))
        ].drop_duplicates(subset="Song")

        # 16곡 추가
        additional_songs = additional_pool.sample(n=min(16, len(additional_pool))).to_dict(orient="records")

        # 최종 리스트 20곡
        final_songs = mix_songs + additional_songs

        return templates.TemplateResponse("list.html", {
            "request": request,
            "songs": final_songs,
            "mood": mood
        })
    except Exception as e:
        import traceback
        print("[ERROR] /list 예외 발생:", traceback.format_exc())
        return JSONResponse(content={"error": "추천 실패"}, status_code=500)
    
# 감정 선택 추천
@app.get("/box1", response_class=HTMLResponse)
async def box1(request: Request):
    return render_box_page(request, mood="행복", title="Happy Mood Playlist")

@app.get("/box2", response_class=HTMLResponse)
async def box2(request: Request):
    return render_box_page(request, mood="중립", title="Sentimental Mood Playlist")

@app.get("/box3", response_class=HTMLResponse)
async def box3(request: Request):
    return render_box_page(request, mood="분노", title="Angry Mood Playlist")

@app.get("/box4", response_class=HTMLResponse)
async def box4(request: Request):
    return render_box_page(request, mood="슬픔", title="Sad Mood Playlist")

