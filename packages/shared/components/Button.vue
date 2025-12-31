<template>
  <button
    :class="['btn', `btn-${variant}`, `btn-${size}`, { 'btn-disabled': disabled }]"
    :disabled="disabled"
    @click="handleClick"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'error'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const handleClick = (event: MouseEvent) => {
  if (!props.disabled) {
    emit('click', event)
  }
}
</script>

<style scoped>
.btn {
  font-family: var(--font-family-base);
  font-weight: 500;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  text-decoration: none;
}

.btn:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.btn-disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Sizes */
.btn-sm {
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-sm);
}

.btn-md {
  padding: 0.75rem 1.5rem;
  font-size: var(--font-size-base);
}

.btn-lg {
  padding: var(--spacing-md) var(--spacing-xl);
  font-size: var(--font-size-lg);
}

/* Variants */
.btn-primary {
  background: var(--color-primary);
  color: var(--color-text-white);
}

.btn-primary:hover:not(.btn-disabled) {
  background: var(--color-primary-dark);
}

.btn-secondary {
  background: var(--color-secondary);
  color: var(--color-text-white);
}

.btn-secondary:hover:not(.btn-disabled) {
  opacity: 0.9;
}

.btn-success {
  background: var(--color-success);
  color: var(--color-text-white);
}

.btn-success:hover:not(.btn-disabled) {
  opacity: 0.9;
}

.btn-warning {
  background: var(--color-warning);
  color: var(--color-text-white);
}

.btn-warning:hover:not(.btn-disabled) {
  opacity: 0.9;
}

.btn-error {
  background: var(--color-error);
  color: var(--color-text-white);
}

.btn-error:hover:not(.btn-disabled) {
  opacity: 0.9;
}
</style>

