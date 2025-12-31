// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },

  imports: {
    autoImport: true
  },

  typescript: {
    strict: false,
    typeCheck: false
  },

  alias: {
    '@shared': '../packages/shared'
  },

  css: ['@shared/styles/index.scss'],

  runtimeConfig: {
    public: {
      supabaseUrl: process.env.SUPABASE_URL || '',
      supabaseKey: process.env.SUPABASE_KEY || ''
    }
  },

  app: {
    head: {
      title: '정보처리기사 카드 문제집',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content: '정보처리기사 문제를 카드 형식으로 학습하는 애플리케이션'
        }
      ],
      link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }]
    }
  }
})
