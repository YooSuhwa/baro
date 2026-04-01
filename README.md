# BARO — 경쟁사 모니터링 & 비교 플랫폼

경쟁사/제품을 등록하면 뉴스가 자동 수집·분류되고, 스펙 변경이 감지되어 관리자 승인 후 반영됩니다.
제품 비교 시 스마트폰 비교 사이트처럼 나란히 비교할 수 있습니다.

## 기술 스택

| 레이어 | 기술 |
|--------|------|
| Backend | FastAPI, SQLAlchemy 2.0 (async), Alembic, PostgreSQL 16, Redis 7 |
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS v4, shadcn/ui |
| AI/LLM | OpenAI API (GPT-4o-mini) |
| Infra | Docker Compose |

## 사전 요구사항

- **Docker Desktop** (PostgreSQL, Redis 실행용)
- **Python 3.12+** & [uv](https://docs.astral.sh/uv/)
- **Node.js 20+** & [pnpm](https://pnpm.io/)

## 빠른 시작

### 1. 인프라 (PostgreSQL + Redis)

```bash
docker compose up -d
```

### 2. Backend

```bash
cd backend

# 환경변수
cp .env.example .env
# .env 파일에서 필요한 API 키 수정 (OpenAI, Naver, Google)

# 의존성 설치
uv sync --all-extras

# DB 마이그레이션
uv run alembic upgrade head

# 서버 실행 (http://localhost:8000)
uv run uvicorn app.main:app --reload --port 8000
```

> **SSL 이슈 시**: 사내 네트워크에서 `SSL_CERT_FILE` 설정이 필요할 수 있습니다.
> ```bash
> cat ~/.ssl/HC_SSL.pem /opt/homebrew/etc/openssl@3/cert.pem > /tmp/combined_ca.pem
> SSL_CERT_FILE=/tmp/combined_ca.pem uv sync --all-extras
> ```

### 3. Frontend

```bash
cd frontend

# 의존성 설치
pnpm install

# 개발 서버 (http://localhost:3000)
pnpm dev
```

### 4. 접속

| URL | 설명 |
|-----|------|
| http://localhost:3000 | Frontend |
| http://localhost:8000/docs | API 문서 (Swagger) |
| http://localhost:8000/redoc | API 문서 (ReDoc) |

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET/POST | `/api/companies` | 경쟁사 목록 / 등록 |
| GET/PUT/DELETE | `/api/companies/:id` | 경쟁사 상세 / 수정 / 삭제 |
| GET | `/api/companies/:id/products` | 회사별 제품 목록 |
| POST | `/api/products` | 제품 등록 |
| GET/PUT/DELETE | `/api/products/:id` | 제품 상세 / 수정 / 삭제 |
| PUT | `/api/products/:id/specs` | 스펙값 일괄 수정 |
| GET | `/api/products/compare?ids=` | 제품 스펙 비교 |
| GET/POST/PUT/DELETE | `/api/spec-fields` | 비교 항목 CRUD |
| GET | `/api/news` | 뉴스 목록 (필터: company_id, sentiment, period) |
| GET | `/api/news/compare?company_ids=` | 뉴스 동향 비교 |
| POST | `/api/news/collect` | 수동 수집 트리거 |
| GET | `/api/spec-changes` | 스펙 변경 요청 목록 |
| PUT | `/api/spec-changes/:id/approve` | 스펙 변경 승인 |
| PUT | `/api/spec-changes/:id/reject` | 스펙 변경 거절 |
| GET | `/api/dashboard/summary` | 대시보드 요약 |

## 테스트

```bash
# Backend (48 tests)
cd backend && uv run pytest -v

# Frontend
cd frontend && pnpm test
```

## 프로젝트 구조

```
baro/
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI 앱
│   │   ├── config.py              # 환경 설정
│   │   ├── core/                  # DB, 예외, 페이지네이션
│   │   └── domains/
│   │       ├── company/           # 경쟁사 CRUD
│   │       ├── product/           # 제품 CRUD + 스펙 비교
│   │       ├── spec_field/        # 비교 항목 관리
│   │       ├── news/              # 뉴스 수집 / 비교
│   │       ├── spec_change/       # 스펙 변경 승인
│   │       └── dashboard/         # 대시보드 집계
│   ├── migrations/                # Alembic
│   └── tests/
├── frontend/
│   └── src/
│       ├── app/                   # Next.js 페이지
│       ├── components/            # shadcn/ui 컴포넌트
│       ├── hooks/queries/         # TanStack Query 훅
│       ├── lib/api/               # API 클라이언트
│       └── types/                 # TypeScript 타입
├── docker-compose.yml
└── docs/PRD.md
```
