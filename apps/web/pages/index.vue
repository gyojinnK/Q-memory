<template>
  <PageLayout size="sm">
    <template #header>
      <h1 class="title">Q Memory</h1>
      <p class="subtitle">정보처리기사 카드 문제집</p>
    </template>

    <SubjectFilter v-model="selectedSubject" />

    <div v-if="loading" class="loading text-center">
      <p>문제를 불러오는 중...</p>
    </div>

    <div v-else-if="error" class="error text-center">
      <p class="text-error">{{ error }}</p>
      <Button variant="primary" size="md" class="mt-md" @click="fetchQuestions">다시 시도</Button>
    </div>

    <div v-else-if="currentQuestion" class="card-container">
      <QuestionCard :question="currentQuestion" @next="handleNext" @previous="handlePrevious" />

      <div class="navigation">
        <Button variant="primary" size="md" :disabled="currentIndex === 0" @click="handlePrevious">
          이전
        </Button>
        <span class="counter">{{ currentIndex + 1 }} / {{ questions.length }}</span>
        <Button
          variant="primary"
          size="md"
          :disabled="currentIndex === questions.length - 1"
          @click="handleNext"
        >
          다음
        </Button>
      </div>
    </div>

    <div v-else class="empty text-center">
      <p class="text-secondary">해당 과목에 문제가 없습니다.</p>
    </div>
  </PageLayout>
</template>

<script setup lang="ts">
import type { Question } from '@q-memory/shared/types'
import { PageLayout } from '@q-memory/shared/layouts'
import { Button } from '@q-memory/shared/components'

// Composable 사용
const { fetchQuestions: getAllQuestions, fetchQuestionsBySubject } = useQuestions()

const questions = ref<Question[]>([])
const currentIndex = ref(0)
const loading = ref(false)
const error = ref<string | null>(null)
const selectedSubject = ref<number | null>(null)

const currentQuestion = computed(() => {
  return questions.value[currentIndex.value] || null
})

const fetchQuestions = async () => {
  loading.value = true
  error.value = null

  try {
    let data: Question[]
    if (selectedSubject.value) {
      data = await fetchQuestionsBySubject(selectedSubject.value)
    } else {
      data = await getAllQuestions()
    }

    questions.value = data

    if (data.length === 0) {
      // 에러보다는 빈 상태로 처리
      // error.value = '문제를 찾을 수 없습니다.'
    }
  } catch (err) {
    error.value = '문제를 불러오는 중 오류가 발생했습니다.'
    console.error('Error fetching questions:', err)
  } finally {
    loading.value = false
  }
}

// 필터 변경 감지
watch(selectedSubject, () => {
  currentIndex.value = 0
  fetchQuestions()
})

const handleNext = () => {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
  }
}

const handlePrevious = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

onMounted(() => {
  fetchQuestions()
})
</script>

<style scoped lang="scss">
.title {
  font-size: var(--font-size-3xl);
  font-weight: bold;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);

  @media (max-width: 768px) {
    font-size: var(--font-size-2xl);
  }
}

.subtitle {
  color: var(--color-text-secondary);
  font-size: var(--font-size-base);

  @media (max-width: 768px) {
    font-size: var(--font-size-sm);
  }
}

.loading,
.error,
.empty {
  padding: var(--spacing-2xl);
}

.card-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xl);
  width: 100%;
  max-width: 600px; /* 태블릿/데스크탑에서 너무 넓어지지 않도록 제한 */
  margin: 0 auto;
}

.navigation {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xl);
  width: 100%;

  @media (max-width: 768px) {
    gap: var(--spacing-md);
  }
}

.counter {
  font-size: var(--font-size-base);
  font-weight: 500;
  color: var(--color-text-secondary);
  width: 80px;
  text-align: center;
}
</style>
