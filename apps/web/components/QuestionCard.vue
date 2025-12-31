<template>
  <FlipCard v-model:flipped="isFlipped" :perspective="1000" class="question-card-wrapper">
    <template #front>
      <div class="question-card-content">
        <div class="question-number">문제 {{ question.id }}</div>
        <div class="question-text">{{ question.question }}</div>
        <div v-if="question.options && question.options.length > 0" class="options">
          <div v-for="(option, index) in question.options" :key="index" class="option">
            {{ String.fromCharCode(65 + index) }}. {{ option }}
          </div>
        </div>
        <div class="hint">카드를 탭하여 정답 확인</div>
      </div>
    </template>
    <template #back>
      <div class="question-card-content">
        <div class="answer-label">정답</div>
        <div class="answer-text">{{ question.answer }}</div>
        <div v-if="question.explanation" class="explanation">
          <div class="explanation-label">해설</div>
          <div class="explanation-text">{{ question.explanation }}</div>
        </div>
      </div>
    </template>
  </FlipCard>
</template>

<script setup lang="ts">
import type { Question } from '@q-memory/shared/types'
import { FlipCard } from '@q-memory/shared/components'

interface Props {
  question: Question
}

const props = defineProps<Props>()

const emit = defineEmits<{
  next: []
  previous: []
}>()

const isFlipped = ref(false)

// 카드가 변경되면 앞면으로 리셋
watch(
  () => props.question.id,
  () => {
    isFlipped.value = false
  }
)
</script>

<style scoped lang="scss">
.question-card-wrapper {
  width: 100%;
  /* 데스크탑 기본 높이 */
  min-height: 600px;
  /* 반응형 높이 설정은 미디어쿼리에서 처리 */
  max-width: 600px;

  :deep(.flip-card-front),
  :deep(.flip-card-back) {
    color: var(--color-text-white);
    /* 모바일에서 패딩 줄임 */
    padding: var(--spacing-xl);

    @media (max-width: 768px) {
      padding: var(--spacing-lg);
    }
  }

  :deep(.flip-card-front) {
    background: var(--color-bg-card-front);
  }

  :deep(.flip-card-back) {
    background: var(--color-bg-card-back);
  }
}

.question-card-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.question-number {
  font-size: var(--font-size-sm);
  opacity: 0.9;
  margin-bottom: var(--spacing-md);
}

.question-text {
  font-size: var(--font-size-xl);
  font-weight: 600;
  line-height: 1.6;
  flex: 1; /* 남은 공간 차지 */
  margin-bottom: var(--spacing-lg);

  @media (max-width: 768px) {
    font-size: var(--font-size-lg);
    margin-bottom: var(--spacing-md);
  }
}

.options {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.option {
  font-size: var(--font-size-base);
  padding: var(--spacing-md);
  background: rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-md);
  backdrop-filter: blur(10px);
  word-break: keep-all; /* 단어 단위 줄바꿈 유지 */
  line-height: 1.4;

  @media (max-width: 768px) {
    font-size: var(--font-size-sm);
    padding: var(--spacing-sm) var(--spacing-md);
  }
}

.hint {
  font-size: var(--font-size-sm);
  opacity: 0.8;
  text-align: center;
  margin-top: auto;
  padding-top: var(--spacing-md);
  border-top: 1px solid rgba(255, 255, 255, 0.3);
}

.answer-label {
  font-size: var(--font-size-sm);
  opacity: 0.9;
  margin-bottom: var(--spacing-md);
}

.answer-text {
  font-size: var(--font-size-3xl);
  font-weight: bold;
  text-align: center;
  margin-bottom: var(--spacing-xl);
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;

  @media (max-width: 768px) {
    font-size: var(--font-size-2xl);
  }
}

.explanation {
  margin-top: auto;
  padding-top: var(--spacing-lg);
  border-top: 1px solid rgba(255, 255, 255, 0.3);
}

.explanation-label {
  font-size: var(--font-size-sm);
  opacity: 0.9;
  margin-bottom: var(--spacing-md);
}

.explanation-text {
  font-size: var(--font-size-base);
  line-height: 1.6;
  opacity: 0.95;
}

@media (max-width: 768px) {
  .question-card-wrapper {
    /* 모바일에서는 높이를 조금 줄임 */
    min-height: 500px;
  }
}
</style>
