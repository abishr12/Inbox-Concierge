import { memo } from "react";
import type { EmailThread } from "@/types";

interface EmailRowProps {
  email: EmailThread;
  labelColorMap: Map<string, string>;
}

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

const EmailRow = memo(({ email, labelColorMap }: EmailRowProps) => {
  const labelColor = labelColorMap.get(email.label_name) || "#6b7280";

  return (
    <>
      <td className="px-4 py-3 bg-amber-100 border-b border-amber-200">
        <span
          className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium text-white"
          style={{ backgroundColor: labelColor }}
        >
          {email.label_name}
        </span>
      </td>
      <td className="px-4 py-3 text-sm text-gray-600 bg-amber-100 border-b border-amber-200">
        {formatDate(email.date)}
      </td>
      <td className="px-4 py-3 text-sm text-gray-900 bg-amber-100 border-b border-amber-200">
        {truncateEmail(email.from)}
      </td>
      <td className="px-4 py-3 min-w-[300px] bg-amber-100 border-b border-amber-200">
        <div className="flex flex-col">
          <span className="text-sm font-medium text-gray-900 break-words">
            {email.subject}
          </span>
          <span className="text-sm text-gray-600 break-words">
            {truncateSnippet(email.snippet)}
          </span>
        </div>
      </td>
    </>
  );
});

EmailRow.displayName = "EmailRow";

export default EmailRow;
