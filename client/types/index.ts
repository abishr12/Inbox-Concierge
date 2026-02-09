export interface EmailThread {
  id: string;
  subject: string;
  snippet: string;
  from: string;
  date: string;
  label_id: string;
  label_name: string;
}

export interface Label extends Bucket {
  color: string;
}

export interface Bucket {
  id: string;
  name: string;
  description: string;
}

export interface AuthStatus {
  authenticated: boolean;
  email?: string;
}
