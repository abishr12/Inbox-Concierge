'use client'

import { useState, useEffect, useCallback, useRef } from 'react'
import type { EmailThread } from '@/types'

const API_BASE = 'http://localhost:8000'

async function consumeSSE(
  url: string,
  method: 'GET' | 'POST',
  onBatch: (batch: EmailThread[]) => void,
  signal?: AbortSignal,
): Promise<void> {
  const response = await fetch(url, { method, signal })

  if (!response.ok) {
    throw new Error(`Failed to fetch: ${response.status}`)
  }

  const reader = response.body?.getReader()
  const decoder = new TextDecoder()

  if (!reader) {
    throw new Error('No reader available')
  }

  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() || ''

    for (const line of lines) {
      if (!line.startsWith('data: ')) continue
      const data = line.slice(6).trim()
      if (!data) continue

      try {
        const batch: EmailThread[] = JSON.parse(data)
        onBatch(batch)
      } catch (e) {
        console.error('Failed to parse SSE data:', e)
      }
    }
  }
}

interface UseEmailsReturn {
  emails: EmailThread[]
  isStreaming: boolean
  isInitialLoad: boolean
  streamCount: number
  recategorize: () => Promise<void>
}

export function useEmails(): UseEmailsReturn {
  const [emails, setEmails] = useState<EmailThread[]>([])
  const [isStreaming, setIsStreaming] = useState(false)
  const [isInitialLoad, setIsInitialLoad] = useState(true)
  const abortRef = useRef<AbortController | null>(null)

  const streamEmails = useCallback(async (url: string, method: 'GET' | 'POST' = 'GET', replace: boolean = false) => {
    // Abort any existing stream
    if (abortRef.current) {
      abortRef.current.abort()
    }
    const controller = new AbortController()
    abortRef.current = controller

    setIsStreaming(true)
    if (replace) {
      setEmails([])
    }

    const accumulated: EmailThread[] = []

    try {
      await consumeSSE(url, method, (batch) => {
        accumulated.push(...batch)
        setEmails([...accumulated])
      }, controller.signal)
    } catch (error) {
      if ((error as Error).name !== 'AbortError') {
        console.error('Stream error:', error)
      }
    } finally {
      setIsStreaming(false)
      setIsInitialLoad(false)
      abortRef.current = null
    }
  }, [])

  // Initial load
  useEffect(() => {
    streamEmails(`${API_BASE}/emails/stream`, 'GET', true)

    return () => {
      if (abortRef.current) {
        abortRef.current.abort()
      }
    }
  }, [streamEmails])

  const recategorize = useCallback(async () => {
    await streamEmails(`${API_BASE}/emails/recategorize-stream`, 'POST', true)
  }, [streamEmails])

  return {
    emails,
    isStreaming,
    isInitialLoad: isInitialLoad && emails.length === 0,
    streamCount: emails.length,
    recategorize,
  }
}
