"use client";

import type { EmailThread, Label } from "@/types";
import { generateRandomColor } from "@/utils/colors";
import { useState } from "react";
import EmailTable from "./components/EmailTable";
import LabelsDropdown from "./components/LabelsDropdown";

const DUMMY_LABELS: Label[] = [
  {
    id: "1",
    name: "Work",
    description: "Work-related emails",
    color: "#3b82f6",
  },
  {
    id: "2",
    name: "Personal",
    description: "Personal correspondence",
    color: "#10b981",
  },
  { id: "3", name: "Important", description: "Urgent items", color: "#ef4444" },
  {
    id: "4",
    name: "Follow-up",
    description: "Needs response",
    color: "#f59e0b",
  },
  { id: "5", name: "Archive", description: "Old emails", color: "#6b7280" },
];

const DUMMY_EMAILS: EmailThread[] = [
  {
    id: "1",
    subject: "Q1 Planning Meeting",
    snippet:
      "Let's discuss the roadmap for next quarter and align on our priorities...",
    from: "alice@company.com",
    to: "me@company.com",
    date: "2026-02-09T10:30:00Z",
    label: "Work",
  },
  {
    id: "2",
    subject: "Project Update: Phase 2",
    snippet:
      "The development team has completed the second phase ahead of schedule...",
    from: "bob@company.com",
    to: "me@company.com",
    date: "2026-02-09T09:15:00Z",
    label: "Work",
  },
  {
    id: "3",
    subject: "Dinner plans this weekend?",
    snippet: "Hey! Would love to catch up. Are you free Saturday evening?",
    from: "charlie@gmail.com",
    to: "me@company.com",
    date: "2026-02-08T18:45:00Z",
    label: "Personal",
  },
  {
    id: "4",
    subject: "URGENT: Server downtime scheduled",
    snippet:
      "Please be aware that we will have planned maintenance tonight from 11 PM...",
    from: "ops@company.com",
    to: "me@company.com",
    date: "2026-02-08T16:20:00Z",
    label: "Important",
  },
  {
    id: "5",
    subject: "Re: Budget proposal feedback",
    snippet:
      "I've reviewed your proposal and have a few questions about the allocation...",
    from: "diana@company.com",
    to: "me@company.com",
    date: "2026-02-08T14:10:00Z",
    label: "Follow-up",
  },
  {
    id: "6",
    subject: "Team building event next month",
    snippet:
      "Save the date! Our annual team building event will be held on March 15th...",
    from: "hr@company.com",
    to: "me@company.com",
    date: "2026-02-07T11:30:00Z",
    label: "Work",
  },
  {
    id: "7",
    subject: "Your monthly newsletter",
    snippet:
      "Check out the latest trends and insights in our industry this month...",
    from: "newsletter@techblog.com",
    to: "me@company.com",
    date: "2026-02-07T08:00:00Z",
    label: "Archive",
  },
  {
    id: "8",
    subject: "Can you review this document?",
    snippet:
      "I've attached the draft specification for the new feature. Would appreciate...",
    from: "eve@company.com",
    to: "me@company.com",
    date: "2026-02-06T15:45:00Z",
    label: "Follow-up",
  },
  {
    id: "9",
    subject: "Congratulations on your promotion!",
    snippet: "Just heard the great news! So happy for you and well deserved...",
    from: "frank@gmail.com",
    to: "me@company.com",
    date: "2026-02-06T12:20:00Z",
    label: "Personal",
  },
  {
    id: "10",
    subject: "Security update required",
    snippet:
      "Action required: Please update your password and enable 2FA by end of week...",
    from: "security@company.com",
    to: "me@company.com",
    date: "2026-02-05T09:00:00Z",
    label: "Important",
  },
  {
    id: "11",
    subject: "Weekly status report",
    snippet:
      "Here is the summary of our team progress for the week ending February 2nd...",
    from: "manager@company.com",
    to: "me@company.com",
    date: "2026-02-04T17:30:00Z",
    label: "Archive",
  },
  {
    id: "12",
    subject: "Coffee chat tomorrow?",
    snippet:
      "Would love to discuss the new project over coffee. Are you available at 10 AM?",
    from: "grace@company.com",
    to: "me@company.com",
    date: "2026-02-04T14:15:00Z",
    label: "Personal",
  },
];

const EmailPage = (): React.ReactElement => {
  const [labels, setLabels] = useState<Label[]>(DUMMY_LABELS);
  const [emails, setEmails] = useState<EmailThread[]>(DUMMY_EMAILS);

  const handleAddLabel = (name: string, description: string): void => {
    const newLabel: Label = {
      id: Date.now().toString(),
      name,
      description,
      color: generateRandomColor(),
    };
    setLabels([...labels, newLabel]);
  };

  const handleDeleteLabel = (labelId: string): void => {
    const labelToDelete = labels.find((l) => l.id === labelId);
    if (!labelToDelete) return;

    setLabels(labels.filter((l) => l.id !== labelId));

    setEmails(
      emails.map((email) =>
        email.label === labelToDelete.name
          ? { ...email, label: "Archive" }
          : email,
      ),
    );
  };

  const handleLogout = (): void => {
    console.log("Logout clicked");
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <LabelsDropdown
              labels={labels}
              onDeleteLabel={handleDeleteLabel}
              onAddLabel={handleAddLabel}
            />

            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow">
          <EmailTable emails={emails} labels={labels} />
        </div>
      </main>
    </div>
  );
};

export default EmailPage;
