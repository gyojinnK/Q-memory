# Supabase 설정 가이드

## 1. Supabase 프로젝트 생성

1. [Supabase](https://supabase.com)에 접속하여 계정 생성/로그인
2. "New Project" 클릭
3. 프로젝트 정보 입력:
   - **Name**: cursor-vibe (또는 원하는 이름)
   - **Database Password**: 강력한 비밀번호 (복사해두세요!)
   - **Region**: Northeast Asia (Seoul) - 한국 서버
   - **Pricing Plan**: Free
4. "Create new project" 클릭 (2-3분 소요)

## 2. 데이터베이스 스키마 생성

1. 프로젝트 대시보드에서 **SQL Editor** 클릭
2. "New query" 클릭
3. `supabase/schema.sql` 파일의 내용을 복사하여 붙여넣기
4. "Run" 버튼 클릭 (또는 Cmd/Ctrl + Enter)
5. 성공 메시지 확인

## 3. API 키 확인

1. 프로젝트 대시보드에서 **Settings** → **API** 클릭
2. 다음 정보를 복사:
   - **Project URL**: `https://xxxxxxxxxxxxx.supabase.co`
   - **anon public** key: `eyJhbGc...` (공개 키, 읽기 전용)
   - **service_role** key: `eyJhbGc...` (비밀 키, 읽기/쓰기)

## 4. 환경 변수 설정

### 4.1 Nuxt 앱 (.env)

```bash
# apps/web/.env 파일 생성
cd apps/web
cat > .env << 'EOF'
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key
EOF
```

### 4.2 크롤러 (.env)

```bash
# services/crawler/.env 파일 생성
cd services/crawler
cat > .env << 'EOF'
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key
EOF
```

> [!WARNING]
> **service_role** 키는 절대 공개하지 마세요! `.gitignore`에 `.env`가 포함되어 있는지 확인하세요.

## 5. 테이블 확인

1. Supabase 대시보드 → **Table Editor** 클릭
2. 다음 테이블이 생성되었는지 확인:
   - `questions` (문제 데이터)
   - `subjects` (과목 정보)

## 6. RLS (Row Level Security) 확인

1. **Table Editor** → `questions` 테이블 클릭
2. "RLS enabled" 배지 확인
3. **Authentication** → **Policies** 에서 정책 확인:
   - "Enable read access for all users" ✅
   - "Enable insert for service role only" ✅

## 7. 다음 단계

- [ ] Nuxt 앱에 Supabase 클라이언트 설치
- [ ] 크롤러에 Supabase Python 클라이언트 설치
- [ ] 크롤러 실행하여 데이터 삽입 테스트

## 트러블슈팅

### "relation already exists" 에러

- 테이블이 이미 존재합니다. 스키마를 다시 실행하기 전에 기존 테이블 삭제:
  ```sql
  DROP TABLE IF EXISTS questions CASCADE;
  DROP TABLE IF EXISTS subjects CASCADE;
  ```

### "permission denied" 에러

- RLS 정책 확인
- Service Role 키를 사용하고 있는지 확인 (크롤러)

### 연결 실패

- SUPABASE_URL이 올바른지 확인
- API 키가 올바른지 확인 (공백 없이 복사)
