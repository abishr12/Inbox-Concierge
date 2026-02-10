"use client";

import { useBuckets } from "@/app/emails/hooks/useBuckets";
import { useEmails } from "@/app/emails/hooks/useEmails";
import { Suspense } from "react";
import EmailTable from "./components/EmailTable";
import LabelsDropdown from "./components/LabelsDropdown";

function LoadingSpinner(): React.ReactElement {
  return (
    <div className="min-h-screen bg-amber-50 flex items-center justify-center">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p className="mt-4 text-gray-600">Loading emails...</p>
      </div>
    </div>
  );
}

function EmailPageContent(): React.ReactElement {
  const {
    emails,
    isStreaming,
    isInitialLoad,
    streamCount,
    recategorize,
  } = useEmails();

  const {
    data: labels,
    isPending: isBucketsPending,
  } = useBuckets();

  const handleLogout = (): void => {
    console.log("Logout clicked");
  };

  // Only show full loading spinner before ANY data arrives
  if (isInitialLoad || isBucketsPending) {
    return <LoadingSpinner />;
  }

  return (
    <div className="min-h-screen bg-amber-50">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <LabelsDropdown
              labels={labels || []}
              onRecategorize={recategorize}
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
          {isStreaming && (
            <div className="flex items-center gap-3 p-4 bg-blue-50 border-b border-blue-200">
              <div className="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
              <p className="text-sm text-blue-800">
                {streamCount === 0
                  ? "Categorizing emails..."
                  : `Categorizing emails... (${streamCount} ready)`}
              </p>
            </div>
          )}
          <EmailTable emails={emails} labels={labels || []} />
        </div>
      </main>
    </div>
  );
}

export default function EmailPage(): React.ReactElement {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <EmailPageContent />
    </Suspense>
  );
}
