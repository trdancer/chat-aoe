export interface ChatResponse {
  timestamp: number,
  response: string,
  entity_names: string[] | null,
  intent: number,
  related_entities: Array<{
    name: string,
    category: string
  }> | null
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

export enum QuestionIntent {
  COST = 0,
  POSSESSION = 1,
  INFO = 2,
  UNIQUE_TECH = 3,
  UNIQUE_UNIT = 4,
  ENTITY_POSSESSION = 5,
}