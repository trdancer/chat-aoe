<script setup lang="ts">
import { computed, ref } from 'vue'
import { CIVILIZATIONS, formatTimestamp } from '@/helpers/constants';
import type { ChatResponse } from '@/types';
import Tag from './Tag.vue';
const props = defineProps<ChatResponse>()
const showAll = ref(false)
const relatedQuestions = ref(
  props.related_entities?.map((e) => {
    if (!CIVILIZATIONS.has(e)) {
      const r = Math.floor(Math.random()*3 % 3)
      switch (r) {
        case 0: return `How much does ${e} cost?`
        case 1: return `Tell me about ${e}.`
        case 2: return `Which civilizations get ${e}?`
        default: `Tell me about ${e}`
      }
    } else {
      const r2 = Math.floor(Math.random()*2 % 2)
      switch (r2) {
        case 0: return `What are ${e}'s unique technologies?`
        case 1: return `What is ${e}'s unique unit?.`
        default: `Tell me about ${e}`
      }
    }
    return `Tell me about ${e}`
  })
)
const questionsToShow = computed(() => {
  if (showAll.value) {
    return relatedQuestions.value
  }
  else {
    const copy = relatedQuestions.value || []
    return copy.slice(0, 5)
  }
})
</script>

<template>
    <div class="dialog-box chat-response">
      <h3 class="chat-header">
        Chat AOE:
      </h3>
      <div v-html="props.response" class="response-text">
      </div>
      <div v-if="props.related_entities && props.related_entities.length > 0">
        <h4>Related Questions</h4>
        <div class="tag-container">
          <Tag v-for="q in questionsToShow" v-bind:content="q"/>
          <div class="tag" @click="showAll = !showAll">
            {{ showAll ? "Less" : "More..." }}
          </div>
        </div>
      </div>
      <div class="time">
        <i>
          {{ formatTimestamp(props.timestamp) }}
        </i>
      </div>
    </div>
</template>

<style scoped>
.chat-response {
  background-color: rgba(235, 235, 235, 0.664);
}
.tag-container {
  display: flex;
  flex-wrap: wrap;
  padding: 0.7rem 0;
}
h4 {
  margin-top: 0.7rem;
  margin-bottom: 0;
}
</style>