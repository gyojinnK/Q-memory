<template>
  <div :class="['container', `container-${size}`]">
    <slot />
  </div>
</template>

<script setup lang="ts">
interface Props {
  size?: 'sm' | 'md' | 'lg'
}

withDefaults(defineProps<Props>(), {
  size: 'md'
})
</script>

<style scoped>
.container {
  width: 100%;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

.container-sm {
  max-width: 800px;
}

.container-md {
  max-width: 1200px;
}

.container-lg {
  max-width: 1400px;
}
</style>

