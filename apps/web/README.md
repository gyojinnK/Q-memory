# 정보처리기사 카드 문제집

정보처리기사 문제를 카드 형식으로 학습할 수 있는 Nuxt 3 애플리케이션입니다.

## 주요 기능

- 📚 정보처리기사 문제 은행 API 연동
- 🎴 카드 형식의 문제/정답 표시
- 🔄 카드 탭으로 앞면/뒷면 전환
- 📱 반응형 디자인

## 기술 스택

- **Framework**: Nuxt 3
- **Language**: TypeScript
- **UI**: Vue 3
- **Styling**: CSS3 (Gradient & 3D Transform)
- **Code Quality**: ESLint, Prettier

## 시작하기

### 설치

```bash
npm install
```

### 개발 서버 실행

```bash
npm run dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000)을 열어 확인하세요.

### 빌드

```bash
npm run build
```

### 프로덕션 미리보기

```bash
npm run preview
```

### 코드 품질 관리

#### ESLint

코드 린팅:

```bash
npm run lint
```

자동 수정:

```bash
npm run lint:fix
```

#### Prettier

코드 포맷팅:

```bash
npm run format
```

포맷팅 확인:

```bash
npm run format:check
```

## 프로젝트 구조

```
.
├── assets/          # CSS 및 정적 자산
├── components/      # Vue 컴포넌트
│   └── QuestionCard.vue
├── pages/          # 페이지 라우트
│   └── index.vue
├── server/          # 서버 API
│   └── api/
│       └── questions.get.ts
├── types/           # TypeScript 타입 정의
│   └── question.ts
├── nuxt.config.ts   # Nuxt 설정
└── package.json
```

## API 연동

실제 정보처리기사 문제 은행 API를 연동하려면:

1. `nuxt.config.ts`에 API URL 설정 추가:
```typescript
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiUrl: process.env.API_URL || 'https://your-api-url.com'
    }
  }
})
```

2. `server/api/questions.get.ts`에서 실제 API 호출로 변경

3. `.env` 파일 생성:
```
API_URL=https://your-api-url.com
```

## 기능 설명

### 카드 플립 애니메이션
- 카드를 클릭하면 3D 회전 효과로 앞면/뒷면이 전환됩니다
- CSS `transform: rotateY()`를 사용한 3D 변환 효과

### 문제 네비게이션
- 이전/다음 버튼으로 문제 간 이동
- 현재 문제 번호 표시

## 라이선스

MIT

