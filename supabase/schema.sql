-- ============================================
-- Supabase Schema for 정보처리기사 문제집
-- ============================================
-- 이 파일을 Supabase SQL Editor에서 실행하세요
-- 또는 Supabase CLI로: supabase db reset
-- ============================================

-- 1. questions 테이블 생성
CREATE TABLE IF NOT EXISTS questions (
  id BIGSERIAL PRIMARY KEY,
  subject INTEGER NOT NULL CHECK (subject >= 1 AND subject <= 5),
  question TEXT NOT NULL,
  options JSONB NOT NULL,
  answer INTEGER NOT NULL CHECK (answer >= 1 AND answer <= 4),
  explanation TEXT DEFAULT '',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_questions_subject ON questions(subject);
CREATE INDEX IF NOT EXISTS idx_questions_created_at ON questions(created_at DESC);

-- 전체 텍스트 검색용 인덱스 (향후 검색 기능용)
CREATE INDEX IF NOT EXISTS idx_questions_question_fts ON questions 
  USING GIN (to_tsvector('simple', question));

-- 3. 트리거: updated_at 자동 업데이트
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_questions_updated_at 
BEFORE UPDATE ON questions
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- 4. Row Level Security (RLS) 설정
ALTER TABLE questions ENABLE ROW LEVEL SECURITY;

-- 모든 사용자에게 읽기 권한 허용
CREATE POLICY "Enable read access for all users" ON questions
  FOR SELECT 
  USING (true);

-- Service Role에만 쓰기 권한 허용 (크롤러용)
CREATE POLICY "Enable insert for service role only" ON questions
  FOR INSERT 
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "Enable update for service role only" ON questions
  FOR UPDATE 
  USING (auth.role() = 'service_role');

CREATE POLICY "Enable delete for service role only" ON questions
  FOR DELETE 
  USING (auth.role() = 'service_role');

-- 5. (선택사항) subjects 테이블 생성
CREATE TABLE IF NOT EXISTS subjects (
  id INTEGER PRIMARY KEY CHECK (id >= 1 AND id <= 5),
  name VARCHAR(100) NOT NULL,
  description TEXT DEFAULT ''
);

-- 초기 데이터 삽입
INSERT INTO subjects (id, name, description) VALUES
  (1, '소프트웨어 설계', '소프트웨어 개발 방법론, 요구사항 분석, 설계 등'),
  (2, '소프트웨어 개발', '데이터 입출력 구현, 통합 구현 등'),
  (3, '데이터베이스 구축', 'SQL 활용, 데이터베이스 설계 등'),
  (4, '프로그래밍 언어 활용', '서버 프로그램 구현, 프로그래밍 언어 활용 등'),
  (5, '정보시스템 구축관리', '소프트웨어 개발 방법론 활용, IT 프로젝트 관리 등')
ON CONFLICT (id) DO NOTHING;

-- subjects 테이블에도 RLS 적용
ALTER TABLE subjects ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable read access for all users on subjects" ON subjects
  FOR SELECT 
  USING (true);

-- 6. 외래 키 제약 조건 추가
ALTER TABLE questions
  DROP CONSTRAINT IF EXISTS fk_subject;

ALTER TABLE questions
  ADD CONSTRAINT fk_subject
  FOREIGN KEY (subject) REFERENCES subjects(id);

-- 7. 유용한 뷰 생성
CREATE OR REPLACE VIEW questions_with_subject_name AS
SELECT 
  q.id,
  q.subject,
  s.name as subject_name,
  q.question,
  q.options,
  q.answer,
  q.explanation,
  q.created_at,
  q.updated_at
FROM questions q
LEFT JOIN subjects s ON q.subject = s.id
ORDER BY q.id;

-- 8. 통계 함수
CREATE OR REPLACE FUNCTION get_question_stats()
RETURNS TABLE (
  total_questions BIGINT,
  questions_by_subject JSONB
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    COUNT(*)::BIGINT as total_questions,
    jsonb_object_agg(subject::text, count) as questions_by_subject
  FROM (
    SELECT subject, COUNT(*) as count
    FROM questions
    GROUP BY subject
  ) subquery;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 완료! 
-- ============================================
-- 다음 단계:
-- 1. Supabase Dashboard → Settings → API에서 URL과 Key 확인
-- 2. .env 파일에 환경 변수 추가
-- 3. 크롤러 실행하여 데이터 삽입
-- ============================================
