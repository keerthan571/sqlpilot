"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import QueryHistory from "@/components/QueryHistory";

export default function QueryWorkspace() {
  const router = useRouter();

  const [question, setQuestion] = useState("");
  const [sql, setSql] = useState("");
  const [rows, setRows] = useState<any[]>([]);
  const [queryExecuted, setQueryExecuted] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [historyRefreshKey, setHistoryRefreshKey] = useState(0);

  const disconnectDatabase = async () => {
    try {
      setLoading(true);
      setError("");

      await api.post("/api/database/disconnect");

      router.push("/connect");
    } catch (error: any) {
      console.error("DISCONNECT ERROR:", error);

      setError(
        error.response?.data?.message ||
        "Unable to disconnect from the database."
      );
    } finally {
      setLoading(false);
    }
  };

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
    <div className="mx-auto max-w-6xl px-4 py-6 sm:px-6 lg:py-10">

      {/* Main Query Workspace */}
      <section className="overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900/80 shadow-xl shadow-black/20">

        {/* Header */}
        <div className="border-b border-zinc-800 px-5 py-5 sm:px-7">

          <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">

            <div>
              <div className="flex items-center gap-3">

                <div className="flex h-11 w-11 items-center justify-center rounded-xl border border-blue-500/20 bg-blue-500/10 text-xl">
                  🚀
                </div>

                <div>
                  <h1 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">
                    SQLPilot
                  </h1>

                  <div className="mt-1 flex items-center gap-2">
                    <span className="h-2 w-2 rounded-full bg-emerald-500" />

                    <span className="text-sm text-zinc-400">
                      Database connected and ready
                    </span>
                  </div>
                </div>

              </div>
            </div>

            <button
              onClick={disconnectDatabase}
              disabled={loading}
              className="self-start rounded-lg border border-red-900/60 bg-red-950/20 px-4 py-2 text-sm font-medium text-red-400 transition hover:border-red-700 hover:bg-red-950/50 disabled:cursor-not-allowed disabled:opacity-50 sm:self-auto"
            >
              Disconnect
            </button>

          </div>

        </div>

        {/* Ask Section */}
        <div className="p-5 sm:p-7">

          <div className="mb-3">
            <label className="text-base font-semibold text-zinc-100">
              Ask your database
            </label>

            <p className="mt-1 text-sm text-zinc-500">
              Describe what you want in plain English. SQLPilot will generate and execute a safe SELECT query.
            </p>
          </div>

          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Example: Show all customers who have placed an order"
            rows={5}
            disabled={loading}
            className="w-full resize-none rounded-xl border border-zinc-700 bg-zinc-950/70 p-4 text-zinc-100 outline-none transition placeholder:text-zinc-600 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 disabled:cursor-not-allowed disabled:opacity-50"
          />

          {/* Examples */}
          <div className="mt-3 flex flex-wrap gap-2">

            <button
              type="button"
              disabled={loading}
              onClick={() => setQuestion("Show all customers")}
              className="rounded-lg border border-zinc-800 bg-zinc-950/40 px-3 py-1.5 text-xs text-zinc-400 transition hover:border-zinc-700 hover:text-zinc-200 disabled:opacity-50"
            >
              Show all customers
            </button>

            <button
              type="button"
              disabled={loading}
              onClick={() =>
                setQuestion("Show customer names and their order amounts")
              }
              className="rounded-lg border border-zinc-800 bg-zinc-950/40 px-3 py-1.5 text-xs text-zinc-400 transition hover:border-zinc-700 hover:text-zinc-200 disabled:opacity-50"
            >
              Customer orders
            </button>

            <button
              type="button"
              disabled={loading}
              onClick={() =>
                setQuestion("Show the total amount of orders for each customer")
              }
              className="rounded-lg border border-zinc-800 bg-zinc-950/40 px-3 py-1.5 text-xs text-zinc-400 transition hover:border-zinc-700 hover:text-zinc-200 disabled:opacity-50"
            >
              Total orders
            </button>

          </div>

          <div className="mt-5 flex flex-col gap-3 border-t border-zinc-800 pt-5 sm:flex-row sm:items-center sm:justify-between">

            <p className="text-xs text-zinc-500">
              Only read-only SELECT queries are allowed.
            </p>

            <button
              onClick={generateQuery}
              disabled={loading || !question.trim()}
              className="rounded-xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-950/30 transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {loading ? "Generating SQL..." : "Generate SQL →"}
            </button>

          </div>

        </div>

      </section>

      {/* Error */}
      {error && (
        <section className="mt-6 rounded-2xl border border-red-900/70 bg-red-950/20 p-5">

          <div className="flex items-start gap-4">

            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-red-500/10 text-lg">
              ⚠️
            </div>

            <div>
              <h2 className="font-semibold text-red-300">
                Query Failed
              </h2>

              <p className="mt-1 text-sm leading-6 text-red-400/80">
                {error}
              </p>
            </div>

          </div>

        </section>
      )}

      {/* Generated SQL */}
      {sql && !error && (
        <section className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900/80 p-5 shadow-xl shadow-black/10 sm:p-6">

          <div className="mb-4 flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-emerald-500/20 bg-emerald-500/10 text-lg">
              {"</>"}
            </div>

            <div>
              <h2 className="font-semibold text-white">
                Generated SQL
              </h2>

              <p className="text-sm text-zinc-500">
                SQL generated from your question
              </p>
            </div>

          </div>

          <pre className="overflow-x-auto rounded-xl border border-zinc-800 bg-zinc-950 p-4 text-sm leading-7 text-emerald-400">
            {sql}
          </pre>

        </section>
      )}

      {/* Query Results */}
      {queryExecuted && !error && (
        <section className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-900/80 p-5 shadow-xl shadow-black/10 sm:p-6">

          <div className="mb-5 flex items-center justify-between gap-4">

            <div>
              <h2 className="text-lg font-semibold text-white">
                Query Results
              </h2>

              <p className="mt-1 text-sm text-zinc-500">
                Results returned from the connected database
              </p>
            </div>

            <span className="shrink-0 rounded-full border border-zinc-700 bg-zinc-800 px-3 py-1.5 text-xs font-medium text-zinc-300">
              {rows.length}{" "}
              {rows.length === 1 ? "row" : "rows"}
            </span>

          </div>

          {rows.length === 0 ? (

            <div className="rounded-xl border border-dashed border-zinc-800 bg-zinc-950/40 p-10 text-center">

              <div className="text-3xl">
                🔍
              </div>

              <p className="mt-3 font-medium text-zinc-300">
                No records found
              </p>

              <p className="mx-auto mt-1 max-w-md text-sm leading-6 text-zinc-500">
                The query executed successfully, but no matching records were found.
              </p>

            </div>

          ) : (

            <div className="overflow-x-auto rounded-xl border border-zinc-800">

              <table className="w-full min-w-max border-collapse text-sm">

                <thead className="bg-zinc-800/80">

                  <tr>
                    {Object.keys(rows[0]).map((key) => (
                      <th
                        key={key}
                        className="border-b border-zinc-700 px-4 py-3 text-left font-semibold text-zinc-200"
                      >
                        {key}
                      </th>
                    ))}
                  </tr>

                </thead>

                <tbody className="divide-y divide-zinc-800 bg-zinc-950/30">

                  {rows.map((row, index) => (
                    <tr
                      key={index}
                      className="transition hover:bg-zinc-800/40"
                    >
                      {Object.values(row).map(
                        (value: any, i) => (
                          <td
                            key={i}
                            className="px-4 py-3 text-zinc-300"
                          >
                            {String(value)}
                          </td>
                        )
                      )}
                    </tr>
                  ))}

                </tbody>

              </table>

            </div>

          )}

        </section>
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