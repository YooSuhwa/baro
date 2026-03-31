# BARO — 경쟁사 모니터링 & 비교 플랫폼

## 프로젝트 구조
- `backend/` — FastAPI (Python 3.12+, uv)
- `frontend/` — Next.js 15 (pnpm, React 19)
- `docs/PRD.md` — 제품 요구사항 문서

## 기술 스택
| 레이어 | 기술 |
|--------|------|
| Backend | FastAPI, SQLAlchemy 2.0 (async), Alembic, PostgreSQL 16, Redis 7 |
| Frontend | Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS v4, shadcn/ui |
| AI/LLM | OpenAI API (GPT-4o-mini), 추상화 레이어로 교체 가능 |
| 비동기 | FastAPI BackgroundTasks + APScheduler (Celery 없이) |
| 테스트 | pytest-asyncio (BE), Vitest + Testing Library + MSW (FE) |
| Infra | Docker Compose (로컬) |

## 로컬 개발
```bash
docker compose up -d  # PostgreSQL + Redis
cd backend && cp .env.example .env && SSL_CERT_FILE=/tmp/combined_ca.pem uv sync --all-extras
SSL_CERT_FILE=/tmp/combined_ca.pem uv run uvicorn app.main:app --reload --port 8000
cd frontend && pnpm install && pnpm dev
```

## 주요 커맨드

### Backend
```bash
cd backend
SSL_CERT_FILE=/tmp/combined_ca.pem uv run pytest                  # 테스트
SSL_CERT_FILE=/tmp/combined_ca.pem uv run pytest --cov=app        # 커버리지
SSL_CERT_FILE=/tmp/combined_ca.pem uv run ruff check app/ tests/  # 린트
SSL_CERT_FILE=/tmp/combined_ca.pem uv run ruff format app/ tests/ # 포맷
SSL_CERT_FILE=/tmp/combined_ca.pem uv run alembic upgrade head    # 마이그레이션
```

### Frontend
```bash
cd frontend
pnpm dev            # 개발 서버 (http://localhost:3000)
pnpm build          # 빌드
pnpm lint           # ESLint
pnpm test           # Vitest
```

## 개발 규칙
- Backend → Frontend 순서 (API 확정 후 프론트엔드)
- P1(MVP) 기능만 구현, P2/P3 미구현, PRD "Not Doing" 항목 구현 금지
- TDD: RED → GREEN → REFACTOR
- 도메인별 파일 구조 (domains/company, domains/product 등)
- DuplicateError 등 에러 코드는 영문 사용 (예: "DUPLICATE_COMPANY")

## SSL 참고
사내 네트워크에서 SSL 인증서 이슈 있음. uv 실행 시 `SSL_CERT_FILE=/tmp/combined_ca.pem` 필요.
combined_ca.pem이 없으면: `cat ~/.ssl/HC_SSL.pem /opt/homebrew/etc/openssl@3/cert.pem > /tmp/combined_ca.pem`
