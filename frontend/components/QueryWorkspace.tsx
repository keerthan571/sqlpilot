"use client";

import { useState } from "react";
import api from "@/lib/api";

export default function QueryWorkspace() {
  const [question, setQuestion] = useState("");
  const [sql, setSql] = useState("");
  const [rows, setRows] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const generateQuery = async () => {
  try {
    console.log("BUTTON CLICKED");
    alert("BUTTON CLICKED");

    setLoading(true);

    const response = await api.post(
      "/api/query/generate",
      {
        question,
      }
    );

    console.log("API RESPONSE:", response.data);

    setSql(response.data.sql);
    setRows(response.data.rows || []);

  } catch (error) {
    console.error("API ERROR:", error);
    alert("API ERROR - check console");

    setSql("");
    setRows([]);
  } finally {
    setLoading(false);
  }
};
  return (
    <div className="mx-auto max-w-6xl p-6">

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
          className="w-full rounded bg-zinc-800 p-4 text-white outline-none"
        />

        <button
          onClick={generateQuery}
          disabled={loading}
          className="mt-4 rounded bg-blue-600 px-6 py-3 text-white hover:bg-blue-700"
        >
          {loading
            ? "Generating..."
            : "Generate SQL"}
        </button>

      </div>

      {sql && (
        <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-900 p-6">

          <h2 className="mb-3 text-xl font-semibold text-white">
            Generated SQL
          </h2>

          <pre className="overflow-x-auto rounded bg-black p-4 text-green-400">
            {sql}
          </pre>

        </div>
      )}

      {rows.length > 0 && (
        <div className="mt-6 rounded-xl border border-zinc-800 bg-zinc-900 p-6">

          <h2 className="mb-4 text-xl font-semibold text-white">
            Query Results
          </h2>

          <div className="overflow-x-auto">

            <table className="w-full border-collapse">

              <thead>
                <tr>
                  {Object.keys(rows[0]).map((key) => (
                    <th
                      key={key}
                      className="border border-zinc-700 bg-zinc-800 p-3 text-left text-white"
                    >
                      {key}
                    </th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {rows.map((row, index) => (
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
                ))}
              </tbody>

            </table>

          </div>

        </div>
      )}

    </div>
  );
}