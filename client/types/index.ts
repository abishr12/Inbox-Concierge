export interface EmailThread {
  id: string;
  subject: string;
  snippet: string;
  from: string;
  to: string;
  date: string;
  label: string;
}

export interface Label {
  id: string;
  name: string;
  description: string;
  color: string;
}

export interface Bucket {
  name: string;
}

export interface AuthStatus {
  authenticated: boolean;
  email?: string;
}
