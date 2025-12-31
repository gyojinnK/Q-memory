// Shared types
export interface Question {
  id: number
  question: string
  answer: string
  options?: string[]
  explanation?: string
  category?: string
  difficulty?: 'easy' | 'medium' | 'hard'
}

export interface QuestionResponse {
  questions: Question[]
  total: number
}

