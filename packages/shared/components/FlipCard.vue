<template>
  <div
    :class="['flip-card-wrapper', { flipped: isFlipped }]"
    :style="{ perspective: `${perspective}px` }"
    :data-clickable="clickable"
    @click="handleClick"
  >
    <div class="flip-card">
      <div class="flip-card-front">
        <slot name="front" />
      </div>
      <div class="flip-card-back">
        <slot name="back" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  flipped?: boolean
  clickable?: boolean
  perspective?: number
}

const props = withDefaults(defineProps<Props>(), {
  flipped: false,
  clickable: true,
  perspective: 1000
})

const emit = defineEmits<{
  'update:flipped': [flipped: boolean]
  flip: [flipped: boolean]
  click: [event: MouseEvent]
}>()

const isFlipped = computed({
  get: () => props.flipped,
  set: value => {
    emit('update:flipped', value)
    emit('flip', value)
  }
})

const handleClick = (event: MouseEvent) => {
  if (props.clickable) {
    isFlipped.value = !isFlipped.value
    emit('click', event)
  }
}
</script>

<style scoped>
.flip-card-wrapper {
  perspective: 1000px;
  width: 100%;
  cursor: pointer;
}

.flip-card-wrapper:not([data-clickable='true']) {
  cursor: default;
}

.flip-card {
  box-sizing: border-box;
  position: relative;
  width: 100%;
  min-height: 100%;
  transform-style: preserve-3d;
  transition: transform var(--transition-slow);
  display: grid;
  grid-template-columns: 100%;
}

.flip-card-wrapper.flipped .flip-card {
  transform: rotateY(180deg);
}

.flip-card-front,
.flip-card-back {
  grid-area: 1 / 1;
  width: 100%;
  min-height: 100%;
  backface-visibility: hidden;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl);
  box-sizing: border-box;
}

.flip-card-back {
  transform: rotateY(180deg);
}
</style>
