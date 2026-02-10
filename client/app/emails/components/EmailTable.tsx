import type { EmailThread, Label } from "@/types";
import { TableVirtuoso } from "react-virtuoso";
import { useMemo, useCallback } from "react";
import EmailRow from "./EmailRow";

interface EmailTableProps {
  emails: EmailThread[];
  labels: Label[];
}

export default function EmailTable({
  emails,
  labels,
}: EmailTableProps): React.ReactElement {
  const labelColorMap = useMemo(() => {
    const map = new Map<string, string>();
    labels.forEach((label) => {
      map.set(label.name, label.color);
    });
    return map;
  }, [labels]);

  const renderRow = useCallback(
    (_index: number, email: EmailThread) => (
      <EmailRow email={email} labelColorMap={labelColorMap} />
    ),
    [labelColorMap]
  );

  return (
    <div className="h-[calc(100vh-12rem)]">
      <TableVirtuoso
        data={emails}
        fixedHeaderContent={() => (
          <tr className="bg-amber-200">
            <th className="text-left px-4 py-3 font-semibold text-sm text-gray-700 border-b border-amber-300 w-[20%]">
              Label
            </th>
            <th className="text-left px-4 py-3 font-semibold text-sm text-gray-700 border-b border-amber-300 w-[12%]">
              Date
            </th>
            <th className="text-left px-4 py-3 font-semibold text-sm text-gray-700 border-b border-amber-300 w-[30%]">
              From
            </th>
            <th className="text-left px-4 py-3 font-semibold text-sm text-gray-700 border-b border-amber-300 w-[38%]">
              Snippet
            </th>
          </tr>
        )}
        itemContent={renderRow}
        components={{
          Table: (props) => (
            <table
              {...props}
              className="w-full border-collapse bg-amber-100"
              style={{ borderSpacing: 0 }}
            />
          ),
          TableRow: (props) => (
            <tr
              {...props}
              className="hover:bg-amber-50 cursor-pointer transition-colors"
            />
          ),
        }}
      />
    </div>
  );
}

