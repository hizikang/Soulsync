from fastapi.templating import Jinja2Templates
import pandas as pd
from models.emotion_model import SentimentAnalyzer

templates = Jinja2Templates(directory="templates")
songs_data = pd.read_csv("data/songs.csv")

# 감정 매핑
MOOD_MAPPING = {
    "Anger": "Angry",
    "Fear": "Sentimental",
    "Happy": "Happy",
    "Tender": "Sentimental",
    "Sad": "Sad"
}

# 감정 피드백 메시지
MOOD_COMMENTS = {
    "Happy": "오늘 당신의 기분은 행복하군요! 신나는 노래로 기분을 더 업그레이드해보세요!",
    "Sentimental": "오늘은 감성적인 하루를 보내고 계신가요? 마음을 따뜻하게 할 노래들을 준비했어요.",
    "Angry": "화가 난 마음, 음악으로 풀어보는 건 어떨까요? 강렬한 비트가 기다리고 있어요!",
    "Sad": "조금 우울한 하루였나요? 감정을 위로해줄 곡을 추천드려요. 편히 쉬면서 들어보세요."
}

analyzer = SentimentAnalyzer()

def analyze_text(user_text: str) -> str:
    if not user_text.strip():
        raise ValueError("입력된 텍스트가 비어 있습니다.")
    return analyzer.analyze_sentiment(user_text)

def render_list_page(request, mood: str):
    try:
        filtered_songs = songs_data[songs_data["Mood"].str.lower() == mood.lower()]
        recommended = filtered_songs.head(12).to_dict(orient="records")
        feedback = MOOD_COMMENTS.get(mood, "오늘의 추천입니다.")
        return templates.TemplateResponse("list.html", {
            "request": request,
            "songs": recommended,
            "mood": mood,
            "feedback": feedback
        })
    except Exception as e:
        return templates.TemplateResponse("list.html", {
            "request": request,
            "songs": [],
            "mood": mood,
            "message": "추천된 노래를 불러오는 데 실패했습니다.",
            "error": str(e)
        })

def render_box_page(request, mood: str, title: str):
    try:
        filtered_songs = songs_data[songs_data["Mood"].str.lower() == mood.lower()]
        selected_songs = filtered_songs.sample(n=min(8, len(filtered_songs))).to_dict(orient="records")
        playlist = selected_songs[:4]
        top_songs = selected_songs[:5]
        return templates.TemplateResponse("box.html", {
            "request": request,
            "playlist": playlist,
            "top_songs": top_songs,
            "title": title,
            "mood": mood
        })
    except Exception as e:
        return templates.TemplateResponse("box.html", {
            "request": request,
            "error": str(e)
        })
