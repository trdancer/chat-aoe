<script setup lang="ts">
import useDefaultStore from '@/store';

const store = useDefaultStore()
const sampleQuestions = [
  "How much does Bloodlines cost?",
  "Tell me about Aztecs.",
  "Do Bengalis get light cav?",
]
</script>

<template>
  <div v-if="store.conversation.length == 0 || store.showHelp" id="help-container">
    <h3>Enter a question in the chat box below!</h3>
    <span>
      Ask questions like:
    </span>
    <ul id="help-list">
      <li v-for="q in sampleQuestions" @click="store.askQuestion(q)">
        {{ q }}
      </li>
    </ul>
  </div>
</template>

<style scoped>
#help-container {
  text-align: center;
}
#help-list {
  list-style-type: none;
  font-style: italic;
  padding-inline-start: 0px;
}

#help-list li {
  text-align: center;
  margin: 10px 0;
}
#help-list li:hover {
  cursor: pointer;
  text-decoration: underline;
}

</style>