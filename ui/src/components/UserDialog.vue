<script setup lang="ts">
import { formatTimestamp } from '@/helpers/constants';
import type { UserQuery } from '@/types';
const props = defineProps<UserQuery>()
</script>

<template>
  <div class="dialog-box">
    <div class="response">
      <h3 class="chat-header">
        You:
      </h3>
      <div>
        {{ props.question }}
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

</style>