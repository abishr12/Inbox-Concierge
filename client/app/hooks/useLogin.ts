'use client'

import { useMutation } from '@tanstack/react-query'

interface LoginResponse {
  auth_url: string
}

export function useLogin() {
  return useMutation({
    mutationFn: async () => {
      const response = await fetch('http://localhost:8000/auth/login')
      if (!response.ok) {
        throw new Error('Failed to initiate login')
      }
      const data: LoginResponse = await response.json()
      return data
    },
    onSuccess: (data) => {
      // Redirect to Google OAuth
      window.location.href = data.auth_url
    },
  })
}
