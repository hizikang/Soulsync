import pandas as pd
import random
from fastapi.templating import Jinja2Templates
from models.emotion_model import SentimentAnalyzer

templates = Jinja2Templates(directory="templates")
songs_data = pd.read_csv("data/songs.csv")

# 감정 : 한글 → 영어 매핑
MOOD_MAPPING = {
    "Happy": "행복",
    "Surprised": "놀람",
    "Angry": "분노",
    "Fearful": "공포",
    "Disgusted": "혐오",
    "Sad": "슬픔",
    "Neutral": "중립"
}

# 감정별 코멘트 (랜덤 선택용)
MOOD_COMMENTS = {
    "행복": [
        "오늘 기분이 행복하군요! 신나는 노래로 더 즐겁게!",
        "행복한 순간에 어울리는 곡을 추천할게요!",
        "미소 짓는 하루, 더 신나게 만들어볼까요?",
        "기분 좋은 하루에 딱 어울리는 음악이에요!",
        "웃음이 나는 날엔 음악도 경쾌하게!"
    ],
    "슬픔": [
        "마음이 무거우셨군요. 위로가 되는 곡들을 준비했어요.",
        "조금 우울한 날엔 감성을 자극하는 음악이 좋아요.",
        "슬픔도 음악으로 다독여보세요.",
        "힘든 하루였나요? 조용히 감싸주는 멜로디를 준비했어요.",
        "눈물이 나올 것 같은 날엔 이 노래를 추천해요."
    ],
    "분노": [
        "속상했던 하루였나요? 강렬한 비트로 날려버려요!",
        "분노가 가득할 땐 이런 음악으로 해소해보세요.",
        "화가 날 땐 묵직한 힙합이 제격이죠!",
        "답답한 감정을 시원하게 날려줄 노래예요.",
        "스트레스 날려줄 강한 리듬의 곡을 추천해요!"
    ],
    "공포": [
        "불안한 감정에는 따뜻한 감성 음악이 어울려요.",
        "불안감을 덜어줄 포근한 곡들을 준비했어요.",
        "무서운 기분, 음악으로 달래보세요.",
        "두려움을 감싸줄 따뜻한 멜로디예요.",
        "마음을 차분하게 가라앉히는 음악이 필요할 때입니다."
    ],
    "혐오": [
        "기분이 좋지 않다면 차분한 음악으로 진정해보세요.",
        "싫은 감정을 조금씩 녹여줄 음악이에요.",
        "혐오감을 씻어내줄 선율을 준비했어요.",
        "불쾌한 하루엔 조용한 음악이 약이죠.",
        "답답한 마음에 작은 위로가 되어줄 곡이에요."
    ],
    "놀람": [
        "조금 놀란 하루였군요. 마음을 안정시켜줄 음악이에요.",
        "예상치 못한 하루, 차분한 곡으로 마무리해보세요.",
        "긴장을 풀어주는 부드러운 음악이에요.",
        "놀란 마음을 가라앉힐 편안한 선율이에요.",
        "심장이 두근거렸다면, 음악으로 리듬을 바꿔보세요."
    ],
    "중립": [
        "오늘은 담담한 하루, 잔잔한 곡들과 함께해요.",
        "평온한 하루엔 부드러운 음악이 잘 어울려요.",
        "기분 좋은 무드는 음악으로 완성되죠.",
        "감정의 흐름 없이 조용히 음악을 즐겨보세요.",
        "무난한 하루엔 차분한 음악이 딱이에요."
    ]
}

analyzer = SentimentAnalyzer()

# 감정 분석 
def analyze_text(text: str) -> str:
    return analyzer.analyze_sentiment(text)

# 감정 기반 노래 리스트 
def render_list_page(request, mood: str):
    try:
        korean_mood = MOOD_MAPPING.get(mood, mood)
        filtered = songs_data[songs_data["Mood"] == korean_mood]
        recommended = filtered.head(3).to_dict(orient="records")
        feedback = random.choice(MOOD_COMMENTS.get(korean_mood, ["오늘의 추천입니다."]))
        return templates.TemplateResponse("list.html", {
            "request": request,
            "songs": recommended,
            "mood": korean_mood,
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

# 고정된 감정 박스 
def render_box_page(request, mood: str, title: str):
    try:
        filtered = songs_data[songs_data["Mood"] == mood]

        if filtered.empty:
            print(f"[WARNING] No songs found for mood: {mood}")

        selected = filtered.sample(n=min(8, len(filtered))).to_dict(orient="records")
        playlist = selected[:4]
        top_songs = selected[:5]

        feedback = random.choice(MOOD_COMMENTS.get(mood, ["추천 음악입니다."]))

        return templates.TemplateResponse("box.html", {
            "request": request,
            "playlist": playlist,
            "top_songs": top_songs,
            "title": title,
            "mood": mood,
            "feedback": feedback
        })
    except Exception as e:
        print(f"[ERROR] box 페이지 렌더링 중 오류 발생: {e}")
        return templates.TemplateResponse("box.html", {
            "request": request,
            "playlist": [],
            "top_songs": [],
            "title": title,
            "mood": mood,
            "feedback": "추천 음악을 불러오는 데 실패했습니다."
        })