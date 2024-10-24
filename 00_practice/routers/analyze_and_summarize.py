from fastapi import APIRouter
from models.input_text import TextInput  # TextInput 모델 가져오기
from services.analyze_and_summarize import perform_sentiment_analysis  # 감정 분석 서비스
from services.analyze_and_summarize import perform_summary  # 요약 서비스

router = APIRouter()

@router.post("/analyze-and-summarize/")
async def analyze_and_summarize(input: TextInput):
    # 감정 분석과 요약 수행
    sentiment = perform_sentiment_analysis(input.text)  # 입력 텍스트에 대해 감정 분석
    summary = perform_summary(input.text)  # 입력 텍스트에 대해 요약
    
    return {
        "summary": summary,
        "sentiment": sentiment
    }
