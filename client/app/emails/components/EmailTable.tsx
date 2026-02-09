import type { EmailThread, Label } from "@/types";

interface EmailTableProps {
  emails: EmailThread[];
  labels: Label[];
}

export default function EmailTable({
  emails,
  labels,
}: EmailTableProps): React.ReactElement {
  const getLabelColor = (labelName: string): string => {
    const label = labels.find((l) => l.name === labelName);
    return label?.color || "#6b7280";
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    const today = new Date();
    const isToday = date.toDateString() === today.toDateString();

    if (isToday) {
      return date.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
      });
    }

    return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
  };

  const truncateEmail = (email: string): string => {
    if (email.length > 30) {
      return email.substring(0, 27) + "...";
    }
    return email;
  };

  const truncateSnippet = (text: string, maxLength: number = 200): string => {
    if (text.length > maxLength) {
      return text.substring(0, maxLength) + "...";
    }
    return text;
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse">
        <thead className="sticky top-0 bg-gray-100 z-10">
          <tr>
            <th className="text-left px-4 py-3 font-semibold text-sm text-gray-700 border-b w-[20%]">
              Label
            </th>
            <th className="text-left px-4 py-3 font-semibold text-sm text-gray-700 border-b w-[12%]">
              Date
            </th>
            <th className="text-left px-4 py-3 font-semibold text-sm text-gray-700 border-b w-[30%]">
              From
            </th>
            <th className="text-left px-4 py-3 font-semibold text-sm text-gray-700 border-b w-[38%]">
              Snippet
            </th>
          </tr>
        </thead>
        <tbody>
          {emails.map((email) => (
            <tr
              key={email.id}
              className="border-b hover:bg-gray-50 cursor-pointer transition-colors"
            >
              <td className="px-4 py-3">
                <span
                  className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium text-white"
                  style={{ backgroundColor: getLabelColor(email.label_name) }}
                >
                  {email.label_name}
                </span>
              </td>
              <td className="px-4 py-3 text-sm text-gray-600">
                {formatDate(email.date)}
              </td>
              <td className="px-4 py-3 text-sm text-gray-900">
                {truncateEmail(email.from)}
              </td>
              <td className="px-4 py-3 min-w-[300px]">
                <div className="flex flex-col">
                  <span className="text-sm font-medium text-gray-900 break-words">
                    {email.subject}
                  </span>
                  <span className="text-sm text-gray-600 break-words">
                    {truncateSnippet(email.snippet)}
                  </span>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
