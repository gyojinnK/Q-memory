<template>
  <div class="subject-filter-container">
    <div class="subject-filter">
      <button
        class="filter-chip"
        :class="{ active: modelValue === null }"
        @click="handleChipClick(null, $event)"
      >
        전체
      </button>
      <button
        v-for="subject in SUBJECTS"
        :key="subject.id"
        class="filter-chip"
        :class="{ active: modelValue === subject.id }"
        @click="handleChipClick(subject.id, $event)"
      >
        {{ subject.name }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { SUBJECTS } from '@q-memory/shared'

interface Props {
  modelValue: number | null
}

defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [value: number | null]
}>()

const handleChipClick = (id: number | null, event: MouseEvent) => {
  emit('update:modelValue', id)

  // 클릭된 요소를 중앙으로 스크롤
  const target = event.currentTarget as HTMLElement
  if (target) {
    target.scrollIntoView({
      behavior: 'smooth',
      inline: 'center',
      block: 'nearest'
    })
  }
}
</script>

<style scoped lang="scss">
.subject-filter-container {
  width: 100%;
  position: relative;
  margin-bottom: var(--spacing-xl);

  /* 마스크 효과: 양 끝이 흐릿하게 */
  mask-image: linear-gradient(
    to right,
    transparent,
    black var(--spacing-xl),
    black calc(100% - var(--spacing-xl)),
    transparent
  );
  -webkit-mask-image: linear-gradient(
    to right,
    transparent,
    black var(--spacing-xl),
    black calc(100% - var(--spacing-xl)),
    transparent
  );
}

.subject-filter {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-xs) var(--spacing-xl); /* 양 끝 여백 */
  overflow-x: auto;
  scroll-behavior: smooth;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE/Edge */

  &::-webkit-scrollbar {
    display: none; /* Chrome/Safari */
  }
}

.filter-chip {
  flex: 0 0 auto; /* 줄바꿈 방지 */
  padding: var(--spacing-xs) var(--spacing-lg);
  border-radius: 100px; /* 둥근 캡슐 형태 */
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;

  /* 기본 상태 (Glassmorphism) */
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--color-text-secondary);
  backdrop-filter: blur(10px);

  &:hover {
    background: rgba(255, 255, 255, 0.2);
    color: var(--color-text-primary);
    transform: translateY(-1px);
  }

  &.active {
    background: var(--color-primary);
    border-color: var(--color-primary);
    color: white;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4); /* Primary glow */
  }
}
</style>
