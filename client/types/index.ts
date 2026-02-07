export interface EmailThread {
  id: string
  subject: string
  snippet: string
  from: string
  date: string
  category: string
}

export interface Bucket {
  name: string
}

export interface AuthStatus {
  authenticated: boolean
  email?: string
}
