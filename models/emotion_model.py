from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class SentimentAnalyzer:
    def __init__(self):
        # KoBERT 토크나이저와 모델 로드
        self.tokenizer = AutoTokenizer.from_pretrained("monologg/kobert", trust_remote_code=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "rkdaldus/ko-sent5-classification", trust_remote_code=True
        )
        self.model.eval()
        self.emotion_labels = ["Anger", "Fear", "Happy", "Tender", "Sad"]

    def analyze_sentiment(self, text: str) -> str:
        if not text.strip():
            raise ValueError("입력된 텍스트가 비어 있습니다.")

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            max_length=128,
            truncation=True,
            padding="max_length"
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            predicted_label = logits.argmax(dim=1).item()
        return self.emotion_labels[predicted_label]
