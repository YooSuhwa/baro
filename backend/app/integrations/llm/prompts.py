SENTIMENT_PROMPT = """뉴스 기사의 감성을 분석하고 한 줄 요약을 생성해주세요.

제목: {title}
본문: {content}

JSON 형식으로 응답해주세요:
{{
  "sentiment": "positive" | "negative" | "neutral",
  "summary": "50자 이내 한 줄 요약"
}}

규칙:
- sentiment: 기업에 긍정적이면 positive, 부정적이면 negative, 중립이면 neutral
- summary: 핵심 내용을 50자 이내로 요약 (한국어)
"""

SPEC_CHANGE_PROMPT = """뉴스 기사에서 제품 스펙 변경 사항을 감지해주세요.

제목: {title}
본문: {content}

감지 대상 제품: {products}

JSON 배열로 응답해주세요:
[
  {{
    "product_name": "제품명",
    "field_name": "변경된 스펙 항목명",
    "old_value_hint": "기존값 (모르면 null)",
    "new_value": "새 값",
    "source_quote": "근거가 되는 원문 인용"
  }}
]

규칙:
- 수치, 버전, 성능 지표 등 구체적인 스펙 변경만 감지
- 추측이 아닌 기사에 명시된 내용만 감지
- 해당 없으면 빈 배열 [] 반환
"""
