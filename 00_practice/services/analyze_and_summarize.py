from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from scipy.special import softmax
import torch, numpy as np

# 감정 분석 모델과 토크나이저 로드
sentiment_model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)

# 요약 모델과 토크나이저 로드
summary_model_name = "eenzeenee/t5-base-korean-summarization"
summarizer_tokenizer = AutoTokenizer.from_pretrained(summary_model_name)
summarizer_model = AutoModelForSeq2SeqLM.from_pretrained(summary_model_name)


translator = pipeline(
    'translation',
    model='facebook/nllb-200-distilled-600M',
    device=-1,
    src_lang='kor_Hang',
    tgt_lang='eng_Latn',
    max_length=256
)


def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

# 번역후 감정 분석
def perform_sentiment_analysis(text: str):
    # 번역 수행
    translated_text = translator(text)[0]['translation_text']

    # 번역된 텍스트를 감정 분석에 맞게 전처리 및 토큰화
    encoded_input = sentiment_tokenizer(translated_text, return_tensors='pt')
    
    # 모델을 사용하여 감정 분석 수행
    output = sentiment_model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    # 감정 점수 랭킹 출력
    ranking = np.argsort(scores)[::-1]
    for i in range(scores.shape[0]):
        label = sentiment_model.config.id2label[ranking[i]]
        score = scores[ranking[i]]
        return f"{i+1}) {label} {np.round(float(score), 4)}"

def perform_summary(text: str) -> str:
    # 입력 텍스트를 토큰화
    inputs = summarizer_tokenizer("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    
    # 모델을 통해 요약 생성
    with torch.no_grad():
        summary_ids = summarizer_model.generate(inputs["input_ids"], num_beams=4, max_length=150, early_stopping=True)
    
    # 요약 결과 디코딩
    summary = summarizer_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    return summary

