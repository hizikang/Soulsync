import torch
from models.emotion_model import SentimentAnalyzer

analyzer = SentimentAnalyzer()

# 감정 분석 함수
def analyze_sentiment(user_text: str) -> str:
    if not user_text.strip():
        raise ValueError("입력된 텍스트가 비어 있습니다.")

    inputs = analyzer.tokenizer(
        user_text,
        return_tensors="pt",
        max_length=128,
        truncation=True,
        padding="max_length"
    )

    with torch.no_grad():
        outputs = analyzer.model(**inputs)
        logits = outputs.last_hidden_state.mean(dim=1)

    predicted_label = logits.argmax(dim=1).item()
    return analyzer.emotion_labels[predicted_label]
