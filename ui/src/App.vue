<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import useDefaultStore from './store';
const store = useDefaultStore()
store.getAppInfo()
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
    <ul>
      <li v-if="store.appInfo.patch">
        <h5>
          Patch {{ store.appInfo.patch }}
        </h5>
      </li>
      <li>
        <RouterLink to="/about" class="no-link-deco">
          <div class="align-horizontal">
            
            <span class="material-symbols-outlined">
              info
            </span>
            About
          </div>
        </RouterLink>
      </li>
    </ul>
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
  padding: 1.1rem 0;
}
ul {
  list-style: none;
  display: flex;
  justify-content: left;
  align-items: center;
}
ul li {
  margin-right: 10px;
}
ul li h5 {
  margin: 0;
}
</style>
