import torch
from transformers import AutoModelForSequenceClassification
from kobert_tokenizer import KoBERTTokenizer

class SentimentAnalyzer:
    def __init__(self):
        # 1. tokenizer 로컬에서 KoBERT 기반으로 불러오기
        self.tokenizer = KoBERTTokenizer.from_pretrained("skt/kobert-base-v1")

        # 2. Hugging Face에 업로드된 파인튜닝 모델 로드
        self.model = AutoModelForSequenceClassification.from_pretrained("hzz15/soulsync")
        self.model.eval()

        # 3. 라벨 매핑 딕셔너리 저장 
        self.label_dict = self.model.config.id2label 

    def analyze_sentiment(self, text: str) -> str:
        # 입력 검증
        text = text.strip()
        if not text or len(text) < 2:
            raise ValueError("입력된 텍스트가 너무 짧거나 비어 있습니다.")

        # 토크나이징
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=128
        )

        print(f"[DEBUG] input_ids: {inputs['input_ids']}")
        print(f"[DEBUG] attention_mask: {inputs.get('attention_mask')}")

        # 예측
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            
            # 여기서 softmax 확률 보기
            probs = torch.nn.functional.softmax(logits, dim=1)
            print("[DEBUG] logits:", logits)
            print("[DEBUG] softmax:", probs)

            pred = torch.argmax(logits, dim=1).item()


        # 라벨 추출
        if str(pred) in self.label_dict:
            emotion = self.label_dict[str(pred)]
        elif pred in self.label_dict:
            emotion = self.label_dict[pred]
        else:
            raise KeyError(f"[ERROR] 라벨 {pred} 이(가) id2label에서 누락됨")

        print(f"[DEBUG] 예측 라벨 ID: {pred} → 감정: {emotion}")
        return emotion

