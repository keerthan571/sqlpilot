"use client";

import { useState } from "react";
import api from "@/lib/api";
import QueryHistory from "@/components/QueryHistory";

export default function QueryWorkspace() {
  const [question, setQuestion] = useState("");
  const [sql, setSql] = useState("");
  const [rows, setRows] = useState<any[]>([]);
  const [queryExecuted, setQueryExecuted] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [historyRefreshKey, setHistoryRefreshKey] = useState(0);

  const generateQuery = async () => {
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setSql("");
      setRows([]);
      setQueryExecuted(false);
      const response = await api.post(
        "/api/query/generate",
        {
          question: question.trim(),
        }
      );

      const data = response.data;

      console.log("API RESPONSE:", data);

      if (!data.success) {
        setError(
          data.error ||
          "Unable to process the query. Please try again."
        );
        return;
      }

      setSql(data.sql || "");
      setRows(data.rows || []);
      setQueryExecuted(true);
      // Refresh history after successful query
      setHistoryRefreshKey(
        (previous) => previous + 1
      );

    } catch (error: any) {
      console.error("API ERROR:", error);

      setSql("");
      setRows([]);

      if (error.response) {
        setError(
          error.response.data?.error ||
          "The server could not process the request."
        );
      } else if (error.request) {
        setError(
          "Unable to connect to SQLPilot backend."
        );
      } else {
        setError(
          "Something went wrong. Please try again."
        );
      }

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-6xl p-6">

      {/* Main Query Box */}
      <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">

        <h1 className="mb-4 text-3xl font-bold text-white">
          SQLPilot 🚀
        </h1>

        <textarea
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          placeholder="Show all customers"
          rows={4}
          disabled={loading}
          className="w-full rounded bg-zinc-800 p-4 text-white outline-none placeholder:text-zinc-500 focus:ring-2 focus:ring-blue-600 disabled:opacity-50"
        />

        <button
          onClick={generateQuery}
          disabled={loading}
          className="mt-4 rounded bg-blue-600 px-6 py-3 text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading
            ? "Generating..."
            : "Generate SQL"}
        </button>

      </div>

      {/* Error */}
      {error && (
        <div className="mt-6 rounded-xl border border-red-900 bg-red-950/40 p-5">

          <div className="flex items-start gap-3">

            <div className="text-xl">
              ⚠️
            </div>

            <div>
              <h2 className="font-semibold text-red-400">
                Query Failed
              </h2>

              <p className="mt-1 text-sm text-red-300">
                {error}
              </p>
            </div>

          </div>

        </div>
      )}

      {/* Generated SQL */}
      {sql && !error && (
        <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-900 p-6">

          <h2 className="mb-3 text-xl font-semibold text-white">
            Generated SQL
          </h2>

          <pre className="overflow-x-auto rounded bg-black p-4 text-green-400">
            {sql}
          </pre>

        </div>
      )}

      {queryExecuted && !error && (
        <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-900 p-6">

          <div className="mb-4 flex items-center justify-between">

            <h2 className="text-xl font-semibold text-white">
              Query Results
            </h2>

            <span className="text-sm text-zinc-400">
              {rows.length}{" "}
              {rows.length === 1 ? "row" : "rows"} returned
            </span>

          </div>

          {rows.length === 0 ? (

            <div className="rounded-lg border border-zinc-800 bg-black p-6 text-center">

              <div className="text-3xl">
                🔍
              </div>

              <p className="mt-3 font-medium text-zinc-300">
                No records found
              </p>

              <p className="mt-1 text-sm text-zinc-500">
                The query executed successfully, but no matching records were found.
              </p>

            </div>

          ) : (

            <div className="overflow-x-auto">

              <table className="w-full border-collapse">

                <thead>
                  <tr>
                    {Object.keys(rows[0]).map(
                      (key) => (
                        <th
                          key={key}
                          className="border border-zinc-700 bg-zinc-800 p-3 text-left text-white"
                        >
                          {key}
                        </th>
                      )
                    )}
                  </tr>
                </thead>

                <tbody>

                  {rows.map(
                    (row, index) => (
                      <tr key={index}>

                        {Object.values(row).map(
                          (value: any, i) => (
                            <td
                              key={i}
                              className="border border-zinc-700 p-3 text-zinc-300"
                            >
                              {String(value)}
                            </td>
                          )
                        )}

                      </tr>
                    )
                  )}

                </tbody>

              </table>

            </div>

          )}

        </div>
      )}

      {/* Query History */}
      <QueryHistory
        refreshKey={historyRefreshKey}
        onUseQuery={(previousQuestion) => {
          setQuestion(previousQuestion);
          setError("");

          window.scrollTo({
            top: 0,
            behavior: "smooth",
          });
        }}
      />

    </div>
  );
}