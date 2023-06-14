<script setup lang="ts">
import useDefaultStore from '@/store';
import { computed, ref } from 'vue'
const userQuery = ref('')
const store = useDefaultStore()
const buttonDisabled = computed(() => userQuery.value === '')
const keyUpAmount = ref(0)
const submitQuestion = () => {
  if (userQuery.value !== '') {
    store.askQuestion(userQuery.value)
    userQuery.value = ''
  }
}

const onKeyUp = () => {
  if (store.conversation.length == 0) {
    return
  }
  if (keyUpAmount.value >= store.conversation.length) {
    userQuery.value = ""
    return
  }
  keyUpAmount.value++
  const i = keyUpAmount.value % store.conversation.length
  const conversation = store.conversation[i]
  const userQuestion = conversation.userQuery.question
  userQuery.value = userQuestion
}

const onKeyDown = () => {
  if (store.conversation.length == 0) {
    return
  }
  if (keyUpAmount.value < 0) {
    userQuery.value = ""
    return
  }
  keyUpAmount.value--
  const i = keyUpAmount.value % store.conversation.length
  const conversation = store.conversation[i]
  const userQuestion = conversation.userQuery.question
  userQuery.value = userQuestion
}

</script>

<template>
  <div id="query-container" >

    <textarea v-model="userQuery" @keyup.enter="submitQuestion" @keyup.up.prevent="onKeyUp" @keyup.down.prevent="onKeyDown" placeholder="What would you like to know?" id="query-box" >
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
  transition: height 0.2s ease-in-out;
}
.submit-button {
  padding: 0.8rem 3rem;
  margin-top: 1rem;
}
textarea:focus-visible {
  outline: #dc9553 inset 2px;
}
@media (max-width: 960px) {
  #query-box:focus-visible {
    height: 5.5rem;
  }
}
</style>