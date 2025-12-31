<template>
  <BaseLayout>
    <template #header>
      <header class="page-header">
        <Container :size="size">
          <slot name="header" />
        </Container>
      </header>
    </template>

    <Container :size="size">
      <slot />
    </Container>

    <template #footer>
      <Container :size="size">
        <slot name="footer" />
      </Container>
    </template>
  </BaseLayout>
</template>

<script setup lang="ts">
import BaseLayout from './BaseLayout.vue'
import Container from '../components/Container.vue'

interface Props {
  size?: 'sm' | 'md' | 'lg'
}

withDefaults(defineProps<Props>(), {
  size: 'sm'
})
</script>

<style scoped>
.page-header {
  padding: var(--spacing-xl) 0;
  text-align: center;
}
</style>
