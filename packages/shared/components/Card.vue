<template>
  <div :class="['card', { 'card-hover': hover, 'card-clickable': clickable }]" @click="handleClick">
    <div v-if="$slots.header" class="card-header">
      <slot name="header" />
    </div>
    <div class="card-body">
      <slot />
    </div>
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  hover?: boolean
  clickable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  hover: false,
  clickable: false
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const handleClick = (event: MouseEvent) => {
  if (props.clickable) {
    emit('click', event)
  }
}
</script>

<style scoped>
.card {
  background: var(--color-bg-primary);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  overflow: hidden;
  transition: all var(--transition-base);
}

.card-hover:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.card-clickable {
  cursor: pointer;
}

.card-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: var(--spacing-lg);
}

.card-footer {
  padding: var(--spacing-lg);
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  background: var(--color-bg-secondary);
}
</style>

