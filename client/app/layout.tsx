import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Email Concierge',
  description: 'AI-powered email categorization',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}): React.ReactElement {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
