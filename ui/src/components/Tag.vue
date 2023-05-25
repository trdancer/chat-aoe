<script setup lang="ts">
import useDefaultStore from '@/store';

const store = useDefaultStore()
const props = defineProps({
  content: {
    type: String,
    required: true,
  }
})
</script>

<template>
  <span class="tag" @click="store.askQuestion(props.content)">
    {{ props.content }}
  </span>
</template>

<style>
.tag {
  padding: 0.5rem 0.9rem;
  margin: 0 5px 5px 0;
  background-color: rgb(255, 198, 112);
  font-size: 0.9rem;
  font-style: italic;
}
.tag:hover {
  cursor: pointer;
  text-decoration: underline;
}
</style>
