import pandas as pd

input_path = "data/emotion_genre_songs.csv"
output_path = "data/emotion_genre_songs_with_kobert_mood.csv" 
df = pd.read_csv(input_path)

# KoBERT 감정 ID 기준 장르 → 감정 매핑
genre_to_mood = {
    "Dance": "행복",        # 0
    "Rock/Metal": "놀람",   # 1
    "Hip-Hop": "분노",      # 2
    "Folk/Blues": "공포",   # 3
    "Indie": "혐오",        # 4
    "Ballad": "슬픔",       # 5
    "R&B/Soul": "중립"      # 6
}

# mood 컬럼 추가
df["mood"] = df["genre"].map(genre_to_mood)

# 저장
df.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"저장 완료: {output_path}")
