export const SUBJECTS = [
  { id: 1, name: '1. 소프트웨어설계' },
  { id: 2, name: '2. 소프트웨어개발' },
  { id: 3, name: '3. 데이터베이스구축' },
  { id: 4, name: '4. 프로그래밍언어활용' },
  { id: 5, name: '5. 정보시스템구축관리' }
] as const

export type SubjectId = (typeof SUBJECTS)[number]['id']
