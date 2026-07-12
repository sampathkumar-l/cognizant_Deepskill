<script setup>
const year = new Date().getFullYear()
</script>

<template>
  <footer class="site-footer">
    <p>&copy; {{ year }} Student Portal &mdash; Digital Nurture 5.0</p>
  </footer>
</template>

<style scoped>
.site-footer {
  text-align: center;
  padding: 1.25rem;
  background: #111827;
  color: #9ca3af;
  font-size: 0.85rem;
}
</style>
