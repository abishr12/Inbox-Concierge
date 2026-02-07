import type { EmailThread } from '@/types'

interface EmailCardProps {
  email: EmailThread
}

export default function EmailCard({ email }: EmailCardProps): React.ReactElement {
  return (
    <div className="p-4 border-b hover:bg-gray-50">
      <h3 className="font-semibold">{email.subject}</h3>
      <p className="text-sm text-gray-600 mt-1">{email.snippet}</p>
      <div className="flex justify-between items-center mt-2 text-xs text-gray-500">
        <span>{email.from}</span>
        <span>{new Date(email.date).toLocaleDateString()}</span>
      </div>
    </div>
  )
}
