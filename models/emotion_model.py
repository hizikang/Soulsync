import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class SentimentAnalyzer:
    def __init__(self):
        # 1. Hugging Face에서 tokenizer 불러오기
        self.tokenizer = AutoTokenizer.from_pretrained("hzz15/soulsync")

        # 2. 파인튜닝된 KoBERT 감정분류 모델 로드
        self.model = AutoModelForSequenceClassification.from_pretrained("hzz15/soulsync")
        self.model.eval()

        # 3. 라벨 매핑 딕셔너리
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
        return emotion

