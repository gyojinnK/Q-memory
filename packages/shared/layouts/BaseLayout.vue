<template>
  <div class="base-layout">
    <header v-if="$slots.header" class="layout-header">
      <slot name="header" />
    </header>
    <main class="layout-main">
      <slot />
    </main>
    <footer v-if="$slots.footer" class="layout-footer">
      <slot name="footer" />
    </footer>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.base-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.layout-header {
  background: var(--color-bg-primary);
  box-shadow: var(--shadow-sm);
  z-index: var(--z-sticky);
  position: sticky;
  top: 0;
}

.layout-main {
  flex: 1;
  padding: var(--spacing-xl) 0;
}

.layout-footer {
  background: var(--color-bg-primary);
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  padding: var(--spacing-lg) 0;
  margin-top: auto;
}
</style>

