// Shared utilities
export const formatQuestionNumber = (num: number): string => {
  return `문제 ${num}`
}

export const getDifficultyColor = (difficulty?: string): string => {
  switch (difficulty) {
    case 'easy':
      return '#4caf50'
    case 'medium':
      return '#ff9800'
    case 'hard':
      return '#f44336'
    default:
      return '#9e9e9e'
  }
}

