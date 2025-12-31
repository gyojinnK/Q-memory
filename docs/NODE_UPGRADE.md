# Node.js 버전 업그레이드 가이드

## 문제 상황

Nuxt 3와 Supabase는 Node.js 18 이상이 필요합니다.
현재 시스템: Node v16.20.2

## 해결 방법

### Option 1: nvm 사용 (추천)

```bash
# 1. nvm 설치 (설치되어 있지 않은 경우)
# macOS/Linux:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 2. 터미널 재시작 또는 nvm 로드
source ~/.zshrc  # 또는 ~/.bashrc

# 3. Node.js 18 LTS 설치
nvm install 18

# 4. Node.js 18 사용
nvm use 18

# 5. 기본 버전으로 설정 (선택사항)
nvm alias default 18

# 6. 버전 확인
node --version  # v18.x.x 출력되어야 함
```

### Option 2: 공식 설치 프로그램

1. [Node.js 공식 사이트](https://nodejs.org/)에서 LTS 버전 (20.x) 다운로드
2. 설치 프로그램 실행
3. 터미널 재시작

### Option 3: Homebrew (macOS)

```bash
# 1. Homebrew로 Node.js 설치
brew install node@20

# 2. PATH에 추가
echo 'export PATH="/usr/local/opt/node@20/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 3. 버전 확인
node --version
```

## 업그레이드 후

```bash
# 1. 기존 node_modules 삭제
rm -rf node_modules apps/web/node_modules packages/*/node_modules

# 2. package-lock.json 삭제
rm -rf package-lock.json apps/web/package-lock.json

# 3. 재설치
npm install

# 4. Supabase 클라이언트 설치
cd apps/web
npm install @supabase/supabase-js
```

## 확인

```bash
# Node 버전 확인
node --version  # 18 이상이어야 함

# npm 버전 확인
npm --version   # 9 이상이어야 함
```
