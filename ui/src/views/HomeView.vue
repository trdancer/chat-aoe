<script setup lang="ts">
import ChatDialog from '../components/ChatDialog.vue'
import ChatBox from '../components/ChatBox.vue'
import Help from '@/components/Help.vue';
import ChatButtonsVue from '@/components/ChatButtons.vue';
</script>

<template>
  <main>
    <div class="inner-container">
      <Help/>
      <ChatButtonsVue/>
      <ChatDialog/>
      <ChatBox/>
    </div>
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: rgba(228, 228, 228, 0.616);
  padding: 30px 50px;
  border-radius: 10px;
}

.inner-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 90%
}
</style>
