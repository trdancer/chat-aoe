<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>

    <div class="wrapper">
      <div id="banner">
        <span class="material-symbols-outlined">forum</span>
        <RouterLink to="/" class="no-link-deco">
          <h1 id="name">Chat AOE</h1>
        </RouterLink>
        <span class="material-symbols-outlined">swords</span>
      </div>
    </div>
  </header>
  
  <RouterView />
  <nav>
    <RouterLink to="/about" class="no-link-deco">
      <div class="align-horizontal">

        <span class="material-symbols-outlined">
          info
        </span>
        About
      </div>
    </RouterLink>
  </nav>
</template>

<style scoped>
header {
  text-align: center;
}
#banner {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
}
#banner > * {
  margin: 0 1%;
}
nav {
  position: relative;
  bottom: 0px;
  padding: 1.2rem 0;
}
</style>
