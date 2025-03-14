from fastapi.responses import JSONResponse, RedirectResponse
from utils.database import get_db_connection

async def login_user(request, username: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return JSONResponse(content={"message": "로그인 실패: 잘못된 아이디 또는 비밀번호"}, status_code=401)
    # 로그인 성공 시 세션에 username 저장
    request.session["username"] = username
    return RedirectResponse(url="/home", status_code=303)

async def signup_user(username: str, password: str, confirm_password: str):
    if password != confirm_password:
        return JSONResponse(content={"message": "비밀번호가 일치하지 않습니다."}, status_code=400)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return JSONResponse(content={"message": "이미 존재하는 아이디입니다."}, status_code=400)
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=302)

def logout_user(request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)
