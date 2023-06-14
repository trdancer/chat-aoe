<script setup lang="ts">
import UserDialogVue from './UserDialog.vue'
import ChatResponseVue from './ChatResponse.vue';
import useDefaultStore from '@/store'
import LoadingVue from './Loading.vue';

const store = useDefaultStore()
// const prevDialogs:Ref<Conversation> = ref([
//     {
//       timestamp: 1684773983,
//       question: "Do byzantines get bloodlines?"
//     },
//     {
//       response: "No, byzantines do not get bloodlines",
//       timestamp: 1684773997,
//       entities: ["Byzantines", "bloodlines"],
//       intent: 1,
//       related_entities: ["Byzantines", "bloodlines"],
//     }
//   ])
// const pushItem = () => {
//   prevDialogs.value.push({
//       timestamp: 1684783983,
//       question: "Do Britons get bloodlines?"
//   })
// }

</script>

<template>
  <div id='chat-container'>
    <TransitionGroup name="dialog">
      <template v-for="{userQuery, chatResponse}, i in store.conversation" class="chat-dialog" >
        <UserDialogVue v-bind="userQuery" />
        <ChatResponseVue v-if="chatResponse" v-bind="chatResponse"/>
      </template>
    </TransitionGroup>
    <div id="anchor"></div>
  </div>
  <LoadingVue v-if="store.loading"/>
</template>

<style scoped>
.chat-dialog {
  min-width: 100%;
  overflow-anchor: none;
}
#chat-container {
  overflow-y: auto;
  max-height: 70vh;
  width: 100%;
  padding-top: 4px;
  border-width: 4px 0;
  border-style: solid;
  border-color: #624224;
}
#anchor {
  overflow-anchor: auto;
  height: 1px;
}

</style>