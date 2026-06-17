"use client";

import { useState } from "react";
import api from "@/lib/api";
import SchemaViewer from "@/components/SchemaViewer";

export default function DatabaseConnectionForm() {
  const [formData, setFormData] = useState({
    db_type: "postgresql",
    host: "localhost",
    port: 5432,
    username: "",
    password: "",
    database: "",
  });

  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<any>(null);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setFormData({
      ...formData,
      [e.target.name]:
        e.target.name === "port"
          ? Number(e.target.value)
          : e.target.value,
    });
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);

      const res = await api.post("/api/database/connect", formData);

      setResponse(res.data);
    } catch (err: any) {
      setResponse({
        success: false,
        message: err.response?.data?.message || err.message,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      {/* Connection Form */}
      <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-8 shadow-xl">
        <h1 className="mb-6 text-3xl font-bold text-white">
          Connect Database
        </h1>

        <div className="space-y-4">
          <select
            name="db_type"
            value={formData.db_type}
            onChange={handleChange}
            className="w-full rounded bg-zinc-800 p-3 text-white"
          >
            <option value="postgresql">PostgreSQL</option>
            <option value="mysql">MySQL</option>
            <option value="sqlite">SQLite</option>
          </select>

          <input
            name="host"
            placeholder="Host"
            value={formData.host}
            onChange={handleChange}
            className="w-full rounded bg-zinc-800 p-3 text-white"
          />

          <input
            name="port"
            type="number"
            value={formData.port}
            onChange={handleChange}
            className="w-full rounded bg-zinc-800 p-3 text-white"
          />

          <input
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            className="w-full rounded bg-zinc-800 p-3 text-white"
          />

          <input
            name="password"
            type="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            className="w-full rounded bg-zinc-800 p-3 text-white"
          />

          <input
            name="database"
            placeholder="Database Name"
            value={formData.database}
            onChange={handleChange}
            className="w-full rounded bg-zinc-800 p-3 text-white"
          />

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-full rounded bg-blue-600 p-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "Connecting..." : "Test Connection"}
          </button>

          {response && (
            <div
              className={`rounded p-4 ${
                response.success
                  ? "bg-green-900 text-green-300"
                  : "bg-red-900 text-red-300"
              }`}
            >
              {response.message}
            </div>
          )}
        </div>
      </div>

      {/* Schema Viewer */}
      {response?.success && response?.schema && (
        <SchemaViewer schema={response.schema} />
      )}
    </div>
  );
}