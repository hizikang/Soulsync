from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from utils.recommendation import analyze_text, MOOD_MAPPING, render_list_page, render_box_page, MOOD_COMMENTS
from fastapi.templating import Jinja2Templates
import pandas as pd

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

@app.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    return render_forgot_password(request)

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

# 추천 관련 라우트
@app.post("/analyze")
async def analyze_endpoint(user_text: str = Form(...)):
    try:
        sentiment = await analyze_text(user_text)  # await 추가!
        return {"text": user_text, "sentiment": sentiment}
    except Exception as e:
        return {"error": f"오류 발생: {str(e)}"}

@app.post("/recommend", response_class=HTMLResponse)
async def recommend_endpoint(request: Request, user_text: str = Form(...)):
    try:
        sentiment = analyze_text(user_text)  # 동기 함수이므로 await 없이 호출
        print(f"분석된 감정: {sentiment}")
        mood = MOOD_MAPPING.get(sentiment)
        if not mood:
            return JSONResponse(
                content={"message": f"'{sentiment}'에 해당하는 노래를 찾을 수 없습니다."},
                status_code=400
            )
        # mood에 해당하는 노래 필터링 및 추천 리스트 생성
        filtered_songs = songs_data[songs_data["Mood"].str.lower() == mood.lower()]
        recommended = filtered_songs.head(12).to_dict(orient="records")
        feedback = MOOD_COMMENTS.get(mood, "오늘의 추천입니다.")
        
        # recommend.html 템플릿을 렌더링해서 이동
        return templates.TemplateResponse("recommend.html", {
            "request": request,
            "songs": recommended,
            "mood": mood,
            "feedback": feedback
        })
    except Exception as e:
        print(f"오류 발생: {e}")
        return JSONResponse(content={"error": f"오류 발생: {str(e)}"}, status_code=500)


@app.get("/box1", response_class=HTMLResponse)
async def box1(request: Request):
    return render_box_page(request, mood="Happy", title="Happy Mood Playlist")

@app.get("/box2", response_class=HTMLResponse)
async def box2(request: Request):
    return render_box_page(request, mood="Sentimental", title="Sentimental Mood Playlist")

@app.get("/box3", response_class=HTMLResponse)
async def box3(request: Request):
    return render_box_page(request, mood="Angry", title="Angry Mood Playlist")

@app.get("/box4", response_class=HTMLResponse)
async def box4(request: Request):
    return render_box_page(request, mood="Sad", title="Sad Mood Playlist")

@app.get("/list", response_class=HTMLResponse)
async def list_page(request: Request, mood: str):
    return render_list_page(request, mood)
