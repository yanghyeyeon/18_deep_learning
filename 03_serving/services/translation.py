from transformers import MBartForConditionalGeneration, MBart50Tokenizer

# 모델 load
model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

# Tokenizer load
tokenizer = MBart50Tokenizer.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")

# 토크나이저 한국어 설정
tokenizer.src_lang = "ko_KR"

def perform_translation(text: str, lang : str) -> str:

    # 토큰화
    encoded_ko = tokenizer(text, return_tensors="pt")
    
    # 추론
    generated_tokens = model.generate(
        **encoded_ko,
        forced_bos_token_id=tokenizer.lang_code_to_id[lang]
    )
    
    # 후처리
    # 번역 결과 decoding
    translated_text = tokenizer.batch_decode(generated_tokens, skip_spcial_tokens=True)
    
    return translated_text[0]