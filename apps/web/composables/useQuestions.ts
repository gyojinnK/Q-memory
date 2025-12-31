import type { Question } from '@q-memory/shared/types'

export const useQuestions = () => {
  /**
   * 모든 문제를 가져옵니다
   */
  const fetchQuestions = async (): Promise<Question[]> => {
    const { data } = await useFetch<Question[]>('/api/questions')
    return data.value || []
  }

  /**
   * 특정 과목의 문제만 가져옵니다
   */
  const fetchQuestionsBySubject = async (subject: number): Promise<Question[]> => {
    const { data } = await useFetch<Question[]>('/api/questions', {
      query: { subject }
    })
    return data.value || []
  }

  /**
   * ID로 특정 문제를 가져옵니다 (임시: 서버 API 추가 필요)
   */
  const fetchQuestionById = async (id: number): Promise<Question | null> => {
    // 단일 조회 API를 만들거나 Supabase 직접 호출을 유지해야 하지만, 아키텍처 통일을 위해
    // 추후 /api/questions/[id] 구현을 권장합니다. 현재는 Supabase 직접 호출을 제거하는 것이 목표이므로
    // 전체 목록에서 찾는 비효율적인 방식보다는, 필요한 경우만 사용하도록 둡니다.
    // 일단은 API 통일성을 위해 비워두거나 TODO 처리합니다.
    const { data } = await useFetch<Question[]>('/api/questions', {
      // 임시로 전체/필터링된 목록에서 찾음 (비권장, 단일 API 필요)
      query: { id } // API가 id 필터링을 지원하도록 수정하면 좋음
    })
    return data.value?.[0] || null
  }

  return {
    fetchQuestions,
    fetchQuestionsBySubject,
    fetchQuestionById
  }
}
