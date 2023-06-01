<script setup lang="ts">
import useDefaultStore from '@/store';
import { computed, ref } from 'vue'
const userQuery = ref('')
const store = useDefaultStore()
const buttonDisabled = computed(() => userQuery.value === '')

const submitQuestion = () => {
  if (userQuery.value !== '') {
    store.askQuestion(userQuery.value)
    userQuery.value = ''
  }
}
</script>

<template>
  <div id="query-container" >

    <textarea v-model="userQuery" @keyup.enter="submitQuestion" placeholder="What would you like to know?" id="query-box" >
    </textarea>
    <button class="submit-button" @click="submitQuestion" :disabled="buttonDisabled">
      Go
    </button>
  </div>
</template>

<style scoped>
#query-container {
  display: flex;
  align-items: center;
  justify-content: left;
  flex-direction: column;
  width: 100%;
  padding: 0.1rem;
  margin: 0.5rem;
}

#query-box {
  background-color: rgba(255, 255, 255, 0.546);
  border-color: #b0b0b0;
  padding: 1rem;
  font-family: inherit;
  font-size: 1.0rem;
  width: 95%;
  height: 3rem;
  resize: vertical;
}
.submit-button {
  padding: 0.8rem 3rem;
  margin-top: 1rem;
}
textarea:focus-visible{
  outline: #dc9553 inset 2px;
}
</style>