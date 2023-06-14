<script setup lang="ts">
import useDefaultStore from '@/store';

const store = useDefaultStore()
</script>

<template>
  <div v-if="store.conversation.length > 0" id="clear-button-container">
    <button @click="store.clearConversation">
      Clear Conversation
      <span class="material-symbols-outlined">
        clear_all
      </span>
    </button>
    <button @click="store.toggleHelp">
      Help
      <span class="material-symbols-outlined">
        help
      </span>
    </button>
  </div>
</template>

<style scoped>
#clear-button-container {
  width: 100%;
  display: flex;
  justify-content: right;
}
#clear-button-container button {
  display: flex;
  align-items: center;
}
#clear-button-container button span {
  margin-left: 5px;
}
@media (max-width: 960px) {
  #clear-button-container {
    justify-content: space-between;
  }
}
</style>