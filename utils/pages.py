from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

templates = Jinja2Templates(directory="templates")

def render_index(request):
    return templates.TemplateResponse("index.html", {"request": request})

def render_login(request):
    return templates.TemplateResponse("login.html", {"request": request})

def render_signup(request):
    return templates.TemplateResponse("signup.html", {"request": request})

def render_home(request):
    username = request.session.get("username", "Guest")
    return templates.TemplateResponse("home.html", {"request": request, "username": username})

def render_welcome(request):
    return templates.TemplateResponse("welcome.html", {"request": request, "username": "로그인 성공!"})

def render_forgot_password(request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})

def render_main(request):
    return templates.TemplateResponse("main.html", {"request": request})

def render_sing(request):
    return templates.TemplateResponse("sing.html", {"request": request})

def render_favicon():
    return FileResponse("static/favicon.ico")

