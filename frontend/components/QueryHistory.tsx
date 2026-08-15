"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";

interface QueryHistoryItem {
  id: number;
  question: string;
  generated_sql: string;
  created_at: string;
}

interface QueryHistoryProps {
  refreshKey: number;
  onUseQuery: (question: string) => void;
}

export default function QueryHistory({
  refreshKey,
  onUseQuery,
}: QueryHistoryProps) {
  const [history, setHistory] = useState<QueryHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  const loadHistory = async () => {
    try {
      setLoading(true);

      const response = await api.get(
        "/api/history"
      );

      setHistory(response.data || []);

    } catch (error) {
      console.error(
        "HISTORY API ERROR:",
        error
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, [refreshKey]);

  return (
    <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-900 p-6">

      <div className="mb-4 flex items-center justify-between">

        <h2 className="text-xl font-semibold text-white">
          Query History
        </h2>

        <button
          onClick={loadHistory}
          className="rounded bg-zinc-800 px-4 py-2 text-sm text-zinc-300 hover:bg-zinc-700"
        >
          Refresh
        </button>

      </div>

      {loading ? (
        <p className="text-zinc-400">
          Loading history...
        </p>
      ) : history.length === 0 ? (
        <p className="text-zinc-500">
          No query history yet.
        </p>
      ) : (
        <div className="space-y-4">

          {history.map((item) => (

            <div
              key={item.id}
              className="rounded-lg border border-zinc-800 bg-black p-4"
            >

              <div className="mb-2 flex items-start justify-between gap-4">

                <div>

                  <p className="font-medium text-white">
                    {item.question}
                  </p>

                  <p className="mt-1 text-xs text-zinc-500">
                    {new Date(
                      item.created_at
                    ).toLocaleString()}
                  </p>

                </div>

                <button
                  onClick={() =>
                    onUseQuery(item.question)
                  }
                  className="shrink-0 rounded bg-blue-600 px-3 py-2 text-sm text-white hover:bg-blue-700"
                >
                  Use Query
                </button>

              </div>

              <pre className="overflow-x-auto rounded bg-zinc-900 p-3 text-sm text-green-400">
                {item.generated_sql}
              </pre>

            </div>

          ))}

        </div>
      )}

    </div>
  );
}