<script setup lang="ts">
import { computed, ref } from 'vue'
import { CIVILIZATIONS, ENTITY_TYPES, formatTimestamp, makeQuestion } from '@/helpers/constants';
import { QuestionIntent, type ChatResponse } from '@/types';
import Tag from './Tag.vue';
const props = defineProps<ChatResponse>()
const showAll = ref(false)
const relatedQuestions = ref(
  props.related_entities?.map(({category, name}) => {
    let r
    switch (category) {
      case ENTITY_TYPES.CIVILIZATION:
        r = Math.floor(0 + (3 - 0) * Math.random())
        switch (r) {
          case 0: return makeQuestion(QuestionIntent.UNIQUE_TECH, name)
          case 1: return makeQuestion(QuestionIntent.UNIQUE_UNIT, name)
          default: return makeQuestion(QuestionIntent.INFO, name)
        }
      case ENTITY_TYPES.TECH:
        r = Math.floor(0 + (3 - 0) * Math.random())
        switch (r) {
          case 0: return makeQuestion(QuestionIntent.COST, name)
          case 1: return makeQuestion(QuestionIntent.INFO, name)
          case 2: return makeQuestion(QuestionIntent.ENTITY_POSSESSION, name)
          default: return makeQuestion(QuestionIntent.INFO, name)
        }
      case ENTITY_TYPES.UNIT:
        r = Math.floor(0 + (3 - 0) * Math.random())
        switch (r) {
          case 0: return makeQuestion(QuestionIntent.COST, name)
          case 1: return makeQuestion(QuestionIntent.INFO, name)
          case 2: return makeQuestion(QuestionIntent.ENTITY_POSSESSION, name)
          default: return makeQuestion(QuestionIntent.INFO, name)
        }
      case ENTITY_TYPES.BUILDING:
        r = Math.floor(0 + (2 - 0) * Math.random())
        switch (r) {
          case 0: return makeQuestion(QuestionIntent.COST, name)
          case 1: return makeQuestion(QuestionIntent.INFO, name)
          default: return makeQuestion(QuestionIntent.INFO, name)
        }
      default: return makeQuestion(QuestionIntent.INFO, name)
    }
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
        <div v-if="props.related_entities.length > 5" class="tag" @click="showAll = !showAll">
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
  padding-top: 0.7rem;
}
h4 {
  margin-top: 0.7rem;
  margin-bottom: 0;
}

</style>