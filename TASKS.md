# BARO(바로) — TASKS

> 경쟁사 실시간 모니터링 & 비교 플랫폼
> PRD: docs/PRD.md | P1(MVP) 기능만 구현
> Plan: .claude/plans/sequential-brewing-lollipop.md

---

## Phase 0: 프로젝트 초기 설정

- [x] Task 0.1: Git 저장소 초기화 (.gitignore)
- [x] Task 0.2: 모노레포 디렉토리 구조 + Docker Compose (PostgreSQL, Redis)
- [x] Task 0.3: Backend 프로젝트 초기화 (FastAPI, pyproject.toml, config, core/database, core/redis, core/models)
- [x] Task 0.4: Alembic 마이그레이션 설정
- [x] Task 0.5: Backend 공통 모듈 (exceptions, exception_handlers, pagination, schemas)
- [x] Task 0.6: Frontend 프로젝트 초기화 (Next.js 15, shadcn/ui, TanStack Query, Vitest)
- [x] Task 0.7: CLAUDE.md 프로젝트 설정

---

## Phase 1: Backend — 데이터 모델 & 핵심 API

- [x] Task 1.1: Company + SearchKeyword 모델 + 테스트 픽스처
- [x] Task 1.2: Company CRUD API (TDD: 5 endpoints, 14 tests)
- [x] Task 1.3: Product + SpecValue 모델 & CRUD API (TDD: 6 endpoints, PUT /products/:id/specs 포함)
- [x] Task 1.4: SpecField 모델 & CRUD API (TDD: 4 endpoints)
- [x] Task 1.5: 제품 스펙 비교 API (GET /products/compare)
- [x] Task 1.6: Alembic 마이그레이션 생성 (Phase 1 모델 일괄)

---

## Phase 2: Backend — 뉴스 수집 & AI 분석

- [ ] Task 2.1: NewsArticle 모델 + 뉴스 API (TDD: 3 endpoints, tags 필드 포함)  ← current
- [ ] Task 2.2: 뉴스 수집 추상화 레이어 (NewsSourceCollector Protocol + Naver/Google)
- [ ] Task 2.3: LLM 추상화 레이어 (LLMProvider Protocol + OpenAI)
- [ ] Task 2.4: SpecChangeRequest 모델 + 승인 API (TDD: 3 endpoints)
- [ ] Task 2.5: 수집 파이프라인 (BackgroundTasks) + 대시보드 API + Phase 2 마이그레이션

---

## Phase 3: Frontend — 레이아웃 & 핵심 페이지

- [ ] Task 3.1: 타입 정의 + API 클라이언트 + 쿼리 키
- [ ] Task 3.2: 앱 레이아웃 + 공통 컴포넌트 (TopNav, SentimentBadge, EmptyState)
- [ ] Task 3.3: 대시보드 페이지 ( / )
- [ ] Task 3.4: 경쟁사 목록 + 상세 페이지 (/companies, /companies/:id)
- [ ] Task 3.5: 경쟁사/제품 등록·수정 폼 (Admin)
- [ ] Task 3.6: 제품 상세 + 비교 항목 관리

---

## Phase 4: Frontend — 비교 & 분석 페이지

- [ ] Task 4.1: 제품 스펙 비교표 (/compare/products)
- [ ] Task 4.2: 뉴스 동향 비교 (/compare/news)
- [ ] Task 4.3: 뉴스 피드 (/news)
- [ ] Task 4.4: 스펙 변경 승인 (/admin/spec-changes)

---

## Phase 5: 통합 & 품질

- [ ] Task 5.1: Docker 빌드 (backend + frontend Dockerfile)
- [ ] Task 5.2: 환경 설정 + README.md
- [ ] Task 5.3: Quality Gate 최종 확인
