'use client'

import { useSuspenseQuery } from '@tanstack/react-query'
import type { EmailThread } from '@/types'

export function useEmails() {
  return useSuspenseQuery({
    queryKey: ['emails'],
    queryFn: async () => {
      const response = await fetch('http://localhost:8000/emails')
      if (!response.ok) {
        throw new Error('Failed to fetch emails')
      }
      const data: EmailThread[] = await response.json()
      return data
    },
  })
}
