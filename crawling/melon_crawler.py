from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# 감정 → 장르
emotion_to_genre = {
    0: "Dance",         # 행복
    1: "Rock/Metal",    # 놀람
    2: "Hip-Hop",       # 분노
    3: "Folk/Blues",    # 공포
    4: "Indie",         # 혐오
    5: "Ballad",        # 슬픔
    6: "R&B/Soul"       # 중립
}

# 장르 → 멜론 코드
genre_code_map = {
    "Ballad": "GN0100",
    "Dance": "GN0200",
    "Hip-Hop": "GN0300",
    "R&B/Soul": "GN0400",
    "Indie": "GN0500",
    "Rock/Metal": "GN0600",
    "Folk/Blues": "GN0800"
}

# Chrome 옵션 설정
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def crawl_melon(genre_code, genre_name, pages=2):
    song_list = []

    for page in range(1, pages + 1):
        url = f"https://www.melon.com/genre/song_list.htm?gnrCode={genre_code}&steadyYn=Y&curPage={page}"
        driver.get(url)
        time.sleep(2)

        rows = driver.find_elements(By.CSS_SELECTOR, '#frm > div > table > tbody > tr')

        for row in rows:
            try:
                title = row.find_element(By.CSS_SELECTOR, 'div.ellipsis.rank01 a').text.strip()
                singer = row.find_element(By.CSS_SELECTOR, 'div.ellipsis.rank02 a').text.strip()
                image = row.find_element(By.CSS_SELECTOR, 'a.image_typeAll img').get_attribute('src')

                song_list.append({
                    "title": title,
                    "singer": singer,
                    "image_url": image,
                    "genre": genre_name
                })
            except Exception as e:
                print("오류 발생:", e)

    return song_list

# 전체 장르별 크롤링 실행
all_songs = []
for emotion_id in range(7):
    genre_name = emotion_to_genre[emotion_id]
    genre_code = genre_code_map[genre_name]
    print(f"🎧 감정 {emotion_id} - {genre_name} 크롤링 중...")
    songs = crawl_melon(genre_code, genre_name, pages=2)
    all_songs.extend(songs)

# DataFrame 생성 및 저장
df = pd.DataFrame(all_songs)
df.to_csv("data/emotion_genre_songs.csv", index=False)
print("저장 완료: emotion_genre_songs.csv")

driver.quit()
