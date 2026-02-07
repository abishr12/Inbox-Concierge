import type { EmailThread } from '@/types'
import EmailCard from './EmailCard'

interface EmailListProps {
  emails: EmailThread[]
  buckets: string[]
}

export default function EmailList({ emails, buckets }: EmailListProps): React.ReactElement {
  const groupedEmails = buckets.reduce((acc, bucket) => {
    acc[bucket] = emails.filter((email) => email.category === bucket)
    return acc
  }, {} as Record<string, EmailThread[]>)

  return (
    <div className="space-y-6">
      {buckets.map((bucket) => (
        <div key={bucket} className="border rounded-lg overflow-hidden">
          <div className="bg-gray-100 px-4 py-3 font-semibold">
            {bucket} ({groupedEmails[bucket].length})
          </div>
          <div>
            {groupedEmails[bucket].map((email) => (
              <EmailCard key={email.id} email={email} />
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
