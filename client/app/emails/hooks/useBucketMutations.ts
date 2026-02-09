'use client'

import { useMutation, useQueryClient } from '@tanstack/react-query'
import type { Bucket } from '@/types'

interface BucketCreate {
  name: string
  description: string
}

interface DeleteBucketResponse {
  success: boolean
  deleted_bucket_id: string
  deleted_bucket_name: string
}

export function useAddBucket() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (bucket: BucketCreate): Promise<Bucket> => {
      const response = await fetch('http://localhost:8000/buckets/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(bucket),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to add bucket')
      }

      return response.json()
    },
    onSuccess: async () => {
      // Refetch both buckets and emails queries immediately
      await Promise.all([
        queryClient.refetchQueries({ queryKey: ['buckets'] }),
        queryClient.refetchQueries({ queryKey: ['emails'] })
      ])
    },
  })
}

export function useDeleteBucket() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (bucketId: string): Promise<DeleteBucketResponse> => {
      const response = await fetch(`http://localhost:8000/buckets/${bucketId}`, {
        method: 'POST',
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to delete bucket')
      }

      return response.json()
    },
    onSuccess: async () => {
      // Refetch both buckets and emails queries immediately
      await Promise.all([
        queryClient.refetchQueries({ queryKey: ['buckets'] }),
        queryClient.refetchQueries({ queryKey: ['emails'] })
      ])
    },
  })
}
