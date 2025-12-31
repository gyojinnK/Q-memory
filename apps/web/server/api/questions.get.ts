import { createClient } from '@supabase/supabase-js'
import type { Question } from '@q-memory/shared/types'

export default defineEventHandler(async (event): Promise<Question[]> => {
  const config = useRuntimeConfig()
  const query = getQuery(event)
  const subject = query.subject as string | undefined

  // Supabase 클라이언트 생성
  const supabase = createClient(config.public.supabaseUrl, config.public.supabaseKey)

  // 쿼리 빌더 생성
  let queryBuilder = supabase.from('questions').select('*').order('id', { ascending: true })

  // 과목 필터링 적용
  if (subject) {
    queryBuilder = queryBuilder.eq('subject', parseInt(subject))
  }

  const { data, error } = await queryBuilder

  if (error) {
    console.error('Failed to fetch questions from Supabase:', error)
    throw createError({
      statusCode: 500,
      message: 'Failed to fetch questions'
    })
  }

  return data as Question[]
})
