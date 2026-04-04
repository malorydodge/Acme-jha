<template>
  <section class="section">
    <div class="container">
      <Navbar />
      <router-view />
    </div>
  </section>
</template>

<script>
import Navbar from './components/Logo.vue'
export default {
  components: {
    Navbar
  }
}
</script>
