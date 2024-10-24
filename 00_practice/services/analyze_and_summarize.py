from transformers import AutoTokenizer, AutoModelForSequenceClassification, T5Tokenizer, T5ForConditionalGeneration
import torch

# 감정 분석 모델과 토크나이저 로드
sentiment_model_name = "Dongjin-kr/ko-reranker"
sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)

# 요약 모델과 토크나이저 로드
summary_model_name = "eenzeenee/t5-base-korean-summarization"
summarizer_tokenizer = T5Tokenizer.from_pretrained(summary_model_name)
summarizer_model = T5ForConditionalGeneration.from_pretrained(summary_model_name)


def perform_sentiment_analysis(text: str) -> dict:
    # 문장을 토큰화 
    encoded_input = sentiment_tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        
    # 모델 예측 수행
    output = sentiment_model(**encoded_input, return_dict=True)
        
    # logits 가져오기
    scores = output.logits.view(-1).float()
        
    # 소프트맥스 변환
    scores = torch.softmax(scores.detach(), dim=0).numpy()
        
    # 감정 레이블 확인
    labels = ['Negative', 'Neutral', 'Positive']  # 실제 레이블에 맞게 조정
        
    # 결과 반환
    # scores가 1차원 배열인지 확인
    if scores.ndim == 1:  # 1차원 배열이면
        return {labels[i]: scores[i].item() for i in range(len(scores))}
    else:
        return {"error": "Unexpected score format"}

# def perform_summary(text: str) -> str:
#     # 입력 텍스트를 토큰화
#     inputs = summarizer_tokenizer("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    
#     # 모델을 통해 요약 생성
#     with torch.no_grad():
#         summary_ids = summarizer_model.generate(inputs["input_ids"], num_beams=4, max_length=150, early_stopping=True)
    
#     # 요약 결과 디코딩
#     summary = summarizer_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
#     return summary
