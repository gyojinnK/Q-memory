# 📝 Q-Memory 프로젝트 히스토리 및 개발 로드맵

이 문서는 MVP 이후의 웹뷰 앱 전환 및 향후 확장 계획을 리마인드하기 위해 작성되었습니다.

## 🏁 현재 진행 상황 (MVP)

1. **자동화 완료**: GitHub Actions를 통해 매일 자정 크롤러가 동작하며 Supabase DB를 최신화합니다.
2. **배포 완료**: Vercel의 `prod` 브랜치를 통해 실제 서비스 중입니다.
3. **웹뷰 착수**: `feat/webview` 브랜치에서 Capacitor 기반의 iOS 환경을 구축했습니다.
   - `ssr: false`, `baseURL: './'` 설정을 통해 하이브리드 앱 호환성을 확보했습니다.
   - Xcode 프로젝트 생성이 완료되었습니다 (`apps/web/ios`).

## 📱 웹뷰(iOS) 다음 작업 단계

다음에 돌아오시면 `feat/webview` 브랜치에서 아래 작업을 이어가면 됩니다.

1. **Native UI 최적화**:
   - 아이폰 노치(Safe Area) 대응을 위한 CSS 수정.
   - 앱 느낌을 주는 스플래시 화면(Splash Screen) 및 아이콘 제작.
2. **Native Bridge 기능**:
   - 카드 뒤집기 시 진동(Haptic Feedback) 추가.
   - 앱 종료 전 뒤로가기 버튼 처리.
3. **리소스 동기화 루틴**:
   - `npx nuxi generate` -> `npx cap sync ios` -> Xcode 실행 순서로 진행.

## 🚀 향후 확장성 (Scalability) 로드맵

이전에 논의했던 프로젝트 확장 아이디어들입니다.

### 1) 개인화 학습 플랫폼 전환

- **Supabase Auth 연동**: 사용자 로그인을 추가하여 개인별 진척도 관리.
- **오답 노트**: 틀린 문제만 따로 모아 보는 로컬 스토리지/DB 기능.
- **학습 통계**: 과목별 정답률 대시보드 시각화.

### 2) AI 기반 학습 도우미

- **AI 해설**: 사용자가 틀린 문제에 대해 LLM(Gemini 등)을 연동하여 보충 설명을 제공.
- **Supabase Edge Functions**: 무거운 AI 연동 로직을 서버리스로 분리하여 성능 최적화.

### 3) 기술적 최적화

- **Lighthouse CI**: 배포 시마다 웹 성능 및 접근성 점수 자동 체크.
- **Cross-Platform**: 동일한 `@q-memory/shared` 패키지를 사용하여 안드로이드 앱 및 태블릿 버전 확장.

---

**Last Updated**: 2026-01-04
**Contact**: Antigravity AI Assistant
