'use client'

import { useSuspenseQuery } from '@tanstack/react-query'
import type { Bucket, Label } from '@/types'
import { generateRandomColor } from '@/utils/colors'

export function useBuckets() {
  return useSuspenseQuery({
    queryKey: ['buckets'],
    queryFn: async () => {
      const response = await fetch('http://localhost:8000/buckets')
      if (!response.ok) {
        throw new Error('Failed to fetch buckets')
      }
      const buckets: Bucket[] = await response.json()
      
      // Transform buckets to labels by adding colors
      const labels: Label[] = buckets.map((bucket) => ({
        ...bucket,
        color: generateRandomColor(),
      }))
      
      return labels
    },
  })
}
