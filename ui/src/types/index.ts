export interface ChatResponse {
  timestamp: number,
  response: string,
  entity_names: string[] | null,
  intent: number,
  related_entities: string[] | null
}

export interface UserQuery {
  question: string,
  timestamp: number,
}

export interface Dialog {
  userQuery: UserQuery,
  chatResponse: undefined | ChatResponse
}
export type Conversation = Dialog[]
