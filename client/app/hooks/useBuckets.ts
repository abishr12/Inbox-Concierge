'use client'

import { useSuspenseQuery } from '@tanstack/react-query'
import type { Bucket, Label } from '@/types'
import { generateColorFromString } from '@/utils/colors'

export function useBuckets() {
  return useSuspenseQuery({
    queryKey: ['buckets'],
    queryFn: async () => {
      const response = await fetch('http://localhost:8000/buckets')
      if (!response.ok) {
        throw new Error('Failed to fetch buckets')
      }
      const buckets: Bucket[] = await response.json()
      
      // Transform buckets to labels by adding deterministic colors
      // Use bucket ID for consistent colors across server/client renders
      const labels: Label[] = buckets.map((bucket) => ({
        ...bucket,
        color: generateColorFromString(bucket.id),
      }))
      
      return labels
    },
  })
}
