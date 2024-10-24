from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# 감정 분석 모델과 토크나이저 로드
sentiment_model_name = "Dongjin-kr/ko-reranker"
sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)

# 요약 모델과 토크나이저 로드
summary_model_name = "eenzeenee/t5-base-korean-summarization"
summarizer_tokenizer = AutoTokenizer.from_pretrained(summary_model_name)
summarizer_model = AutoModelForSeq2SeqLM.from_pretrained(summary_model_name)

# 번역 모델과 토크나이저 로드
model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def perform_sentiment_analysis(text: str) -> dict:
    # 텍스트를 토크나이즈하고 모델에 입력
    inputs = tokenizer(text, return_tensors="pt", padding=True)

    # 번역 수행
    translated_tokens = model.generate(**inputs)
    
    # 번역된 텍스트 디코딩
    english_translation = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    
    print(english_translation)

    # 번역된 텍스트 디코딩
    english_translation = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

def perform_summary(text: str) -> str:
    # 입력 텍스트를 토큰화
    inputs = summarizer_tokenizer("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    
    # 모델을 통해 요약 생성
    with torch.no_grad():
        summary_ids = summarizer_model.generate(inputs["input_ids"], num_beams=4, max_length=150, early_stopping=True)
    
    # 요약 결과 디코딩
    summary = summarizer_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    return summary

