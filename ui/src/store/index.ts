import type { ChatResponse, Conversation, UserQuery } from '@/types'
import { apiUrl } from '../helpers/constants'
import { defineStore } from 'pinia'
import axios from 'axios'
import dayjs from 'dayjs'

interface DefaultStore {
  conversation: Conversation,
  userQuery: undefined | UserQuery,
  chatResponse: undefined | ChatResponse
  loading: boolean,
  error: undefined | string,
  showHelp: boolean,
  appInfo: {
    patch: string,
  }
}
const useDefaultStore = defineStore(
  'myStore',
  {
    state: ():DefaultStore => {
      return {
        conversation: [],
        userQuery: undefined,
        chatResponse: undefined,
        loading: false,
        error: undefined,
        showHelp: false,
        appInfo: {
          patch: ""
        },
      }
    },
    actions: {
      async askQuestion(question:string) {
        this.loading = true
        this.conversation.push({
          userQuery: {
            timestamp: dayjs().unix(),
            question,
          },
          chatResponse: undefined
        })
        const i = this.conversation.length - 1
        try {
          const url = `${apiUrl}chat`
          const response = await axios.get(url, {
            params: {
              q: question
            }
          })
          const chatResponse = response.data
          this.conversation[i].chatResponse = {...chatResponse, timestamp: dayjs().unix()}
          this.loading = false
          this.error = undefined
        } catch (err) {
          this.loading = false
          this.error = 'Failed to connect to the API'
          this.conversation[i].chatResponse = {
            response: "I couldn't quite understand that, please try again",
            entity_names: [],
            intent: -1,
            related_entities: [], 
            timestamp: dayjs().unix(),
          }
          console.log(err)
        }
      },
      clearConversation() {
        this.conversation = []
      },
      toggleHelp() {
        this.showHelp = !this.showHelp
      },
      async getAppInfo() {
        const url = `${apiUrl}/info`
        try {
          const response = await axios.get(url)
          this.appInfo.patch = response.data.patch
        } catch (e) {
          this.appInfo.patch = "Error"
          console.log(e)
        }

      }
    }
  }

)
export default useDefaultStore