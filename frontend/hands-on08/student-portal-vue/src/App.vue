<script setup>
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
</script>

<template>
  <Header />
  <main class="app-main">
    <!-- Step 113: RouterView renders whichever route is currently matched -->
    <RouterView />
  </main>
  <Footer />
</template>

<style scoped>
.app-main {
  min-height: 70vh;
}
</style>
