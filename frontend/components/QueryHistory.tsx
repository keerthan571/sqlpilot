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

const INITIAL_HISTORY_COUNT = 5;

export default function QueryHistory({
  refreshKey,
  onUseQuery,
}: QueryHistoryProps) {
  const [history, setHistory] = useState<QueryHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAll, setShowAll] = useState(false);

  const loadHistory = async () => {
    try {
      setLoading(true);

      const response = await api.get("/api/history");

      setHistory(response.data || []);
    } catch (error) {
      console.error("HISTORY API ERROR:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, [refreshKey]);

  const visibleHistory = showAll
    ? history
    : history.slice(0, INITIAL_HISTORY_COUNT);

  return (
    <section className="mt-8 rounded-2xl border border-zinc-800 bg-zinc-900/80 p-5 shadow-xl shadow-black/20 sm:p-6">

      {/* Header */}
      <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">

        <div>
          <div className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-blue-500/20 bg-blue-500/10 text-lg">
              🕘
            </div>

            <div>
              <h2 className="text-lg font-semibold text-white">
                Query History
              </h2>

              <p className="text-sm text-zinc-500">
                {history.length}{" "}
                {history.length === 1
                  ? "saved query"
                  : "saved queries"}
              </p>
            </div>

          </div>
        </div>

        <button
          onClick={loadHistory}
          disabled={loading}
          className="rounded-lg border border-zinc-700 bg-zinc-800 px-4 py-2 text-sm font-medium text-zinc-300 transition hover:border-zinc-600 hover:bg-zinc-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? "Refreshing..." : "Refresh"}
        </button>

      </div>

      {/* Loading */}
      {loading ? (

        <div className="rounded-xl border border-zinc-800 bg-black/30 p-8 text-center">
          <div className="text-sm text-zinc-400">
            Loading query history...
          </div>
        </div>

      ) : history.length === 0 ? (

        <div className="rounded-xl border border-dashed border-zinc-800 bg-black/20 p-10 text-center">

          <div className="text-3xl">
            🗂️
          </div>

          <p className="mt-3 font-medium text-zinc-300">
            No query history yet
          </p>

          <p className="mt-1 text-sm text-zinc-500">
            Your successful queries will appear here.
          </p>

        </div>

      ) : (

        <>
          <div className="space-y-3">

            {visibleHistory.map((item) => (

              <div
                key={item.id}
                className="group rounded-xl border border-zinc-800 bg-black/40 p-4 transition hover:border-zinc-700 hover:bg-black/60"
              >

                <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">

                  <div className="min-w-0 flex-1">

                    <p className="truncate font-medium text-zinc-100">
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
                    className="shrink-0 rounded-lg border border-blue-500/30 bg-blue-600/10 px-3 py-2 text-sm font-medium text-blue-400 transition hover:bg-blue-600 hover:text-white"
                  >
                    Use Query →
                  </button>

                </div>

                <div className="mt-3 overflow-hidden rounded-lg border border-zinc-800 bg-zinc-950">

                  <pre className="max-h-20 overflow-auto p-3 text-xs leading-6 text-emerald-400">
                    {item.generated_sql}
                  </pre>

                </div>

              </div>

            ))}

          </div>

          {/* Show More / Less */}
          {history.length > INITIAL_HISTORY_COUNT && (

            <div className="mt-5 flex justify-center">

              <button
                onClick={() =>
                  setShowAll((previous) => !previous)
                }
                className="rounded-lg border border-zinc-700 bg-zinc-800 px-5 py-2 text-sm font-medium text-zinc-300 transition hover:bg-zinc-700"
              >
                {showAll
                  ? "Show Less"
                  : `Show All ${history.length} Queries`}
              </button>

            </div>

          )}

        </>

      )}

    </section>
  );
}