"use client";

import { useBuckets } from "@/app/hooks/useBuckets";
import { useEmails } from "@/app/hooks/useEmails";
import { Suspense } from "react";
import EmailTable from "./components/EmailTable";
import LabelsDropdown from "./components/LabelsDropdown";

function LoadingSpinner(): React.ReactElement {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p className="mt-4 text-gray-600">Loading emails...</p>
      </div>
    </div>
  );
}

function EmailPageContent(): React.ReactElement {
  const { data: emails } = useEmails();
  const { data: labels } = useBuckets();

  const handleLogout = (): void => {
    console.log("Logout clicked");
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <LabelsDropdown labels={labels} />

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
}

export default function EmailPage(): React.ReactElement {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <EmailPageContent />
    </Suspense>
  );
}
