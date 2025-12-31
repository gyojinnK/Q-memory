# Q Memory (정보처리기사 카드 문제집)

정보처리기사 문제를 카드 형식으로 학습할 수 있는 Nuxt 3 모노레포 애플리케이션입니다.

## 프로젝트 구조

```
q-memory/
├── apps/
│   └── web/              # Nuxt 3 웹 애플리케이션
├── packages/
│   └── shared/           # 공유 타입 및 유틸리티
├── package.json          # 루트 워크스페이스 설정
└── ...
```

## 주요 기능

- 📚 정보처리기사 문제 은행 API 연동
- 🎴 카드 형식의 문제/정답 표시
- 🔄 카드 탭으로 앞면/뒷면 전환
- 📱 반응형 디자인
- 🏗️ 모노레포 구조로 확장 가능한 아키텍처

## 기술 스택

- **Framework**: Nuxt 3
- **Language**: TypeScript
- **UI**: Vue 3
- **Styling**: CSS3 (Gradient & 3D Transform)
- **Code Quality**: ESLint, Prettier
- **Monorepo**: npm workspaces

## 시작하기

### 설치

```bash
npm install
```

### 개발 서버 실행

```bash
npm run dev
```

또는 특정 워크스페이스에서 실행:

```bash
npm run dev --workspace=apps/web
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

## 워크스페이스

### apps/web

Nuxt 3 웹 애플리케이션

### packages/shared

공유 타입, 유틸리티, 컴포넌트, 레이아웃 및 스타일

#### 타입 및 유틸리티

```typescript
// 타입 사용 예시
import type { Question } from '@q-memory/shared/types'

// 유틸리티 사용 예시
import { formatQuestionNumber } from '@q-memory/shared/utils'
```

#### 공용 컴포넌트

```vue
<script setup>
import { Button, Card, Container } from '@q-memory/shared/components'
</script>

<template>
  <Container size="sm">
    <Card hover>
      <template #header>
        <h2>제목</h2>
      </template>
      <p>내용</p>
      <template #footer>
        <Button variant="primary" @click="handleClick">확인</Button>
      </template>
    </Card>
  </Container>
</template>
```

#### 공용 레이아웃

```vue
<script setup>
import { PageLayout } from '@q-memory/shared/layouts'
</script>

<template>
  <PageLayout size="sm">
    <template #header>
      <h1>페이지 제목</h1>
    </template>

    <p>페이지 내용</p>

    <template #footer>
      <p>푸터</p>
    </template>
  </PageLayout>
</template>
```

#### 공용 스타일

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  css: ['@shared/styles/index.css']
})
```

CSS 변수 사용:

```css
.my-component {
  color: var(--color-primary);
  padding: var(--spacing-md);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}
```

## 코드 품질 관리

### ESLint

코드 린팅:

```bash
npm run lint
```

자동 수정:

```bash
npm run lint:fix
```

### Prettier

코드 포맷팅:

```bash
npm run format
```

포맷팅 확인:

```bash
npm run format:check
```

## 모노레포 명령어

### 모든 워크스페이스에서 실행

```bash
npm run <script> --workspaces
```

### 특정 워크스페이스에서 실행

```bash
npm run <script> --workspace=apps/web
npm run <script> --workspace=packages/shared
```

## API 연동

실제 정보처리기사 문제 은행 API를 연동하려면:

1. `apps/web/nuxt.config.ts`에 API URL 설정 추가:

```typescript
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiUrl: process.env.API_URL || 'https://your-api-url.com'
    }
  }
})
```

2. `apps/web/server/api/questions.get.ts`에서 실제 API 호출로 변경

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
