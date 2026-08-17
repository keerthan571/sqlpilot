"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import SchemaViewer from "@/components/SchemaViewer";

interface ConnectionResponse {
  success: boolean;
  message: string;
  database_type?: string;
  schema?: Record<string, unknown>;
}

interface SavedConnection {
  id: number;
  name: string;
  db_type: string;
  host: string;
  port: number;
  username: string;
  database_name: string;
  created_at: string;
}

const DATABASES = [
  {
    value: "postgresql",
    name: "PostgreSQL",
    description: "Recommended",
    icon: "🐘",
  },
  {
    value: "mysql",
    name: "MySQL",
    description: "Relational database",
    icon: "🐬",
  },
  {
    value: "sqlite",
    name: "SQLite",
    description: "Local database",
    icon: "📦",
  },
];

export default function DatabaseConnectionForm() {
  const router = useRouter();

  const [formData, setFormData] = useState({
    db_type: "postgresql",
    host: "localhost",
    port: 5432,
    username: "",
    password: "",
    database: "",
  });

  const [loading, setLoading] = useState(false);

  const [response, setResponse] =
    useState<ConnectionResponse | null>(null);

  const [savedConnections, setSavedConnections] =
    useState<SavedConnection[]>([]);

  const [loadingSaved, setLoadingSaved] =
    useState(true);

  const [reconnectingId, setReconnectingId] =
    useState<number | null>(null);

  const [deletingId, setDeletingId] =
    useState<number | null>(null);

  useEffect(() => {
    loadSavedConnections();
  }, []);

  const loadSavedConnections = async () => {
    try {
      setLoadingSaved(true);

      const res = await api.get(
        "/api/database/saved"
      );

      setSavedConnections(res.data);
    } catch (error) {
      console.error(
        "Failed to load saved connections:",
        error
      );
    } finally {
      setLoadingSaved(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const { name, value } = e.target;

    setFormData((previous) => ({
      ...previous,
      [name]:
        name === "port"
          ? Number(value)
          : value,
    }));

    if (response) {
      setResponse(null);
    }
  };

  const handleDatabaseType = (type: string) => {
    setFormData((previous) => ({
      ...previous,
      db_type: type,
      port:
        type === "postgresql"
          ? 5432
          : type === "mysql"
            ? 3306
            : 0,
    }));

    if (response) {
      setResponse(null);
    }
  };

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setResponse(null);

      const res = await api.post(
        "/api/database/connect",
        formData
      );

      setResponse(res.data);

      if (res.data.success) {
        await loadSavedConnections();
      }
    } catch (err: any) {
      setResponse({
        success: false,
        message:
          err.response?.data?.message ||
          "Unable to connect to the database.",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleReconnect = async (
    connectionId: number
  ) => {
    try {
      setReconnectingId(connectionId);
      setResponse(null);

      const res = await api.post(
        `/api/database/reconnect/${connectionId}`
      );

      setResponse(res.data);
    } catch (err: any) {
      setResponse({
        success: false,
        message:
          err.response?.data?.message ||
          "Unable to reconnect to the database.",
      });
    } finally {
      setReconnectingId(null);
    }
  };

  const handleDelete = async (
    connectionId: number
  ) => {
    try {
      setDeletingId(connectionId);

      await api.delete(
        `/api/database/saved/${connectionId}`
      );

      setSavedConnections((previous) =>
        previous.filter(
          (connection) =>
            connection.id !== connectionId
        )
      );
    } catch (err: any) {
      setResponse({
        success: false,
        message:
          err.response?.data?.message ||
          "Unable to remove the saved connection.",
      });
    } finally {
      setDeletingId(null);
    }
  };

  const getDatabaseInfo = (
    type: string
  ) => {
    return (
      DATABASES.find(
        (database) =>
          database.value === type
      ) || {
        name: type,
        icon: "🗄️",
      }
    );
  };

  return (
    <main className="min-h-screen bg-[#050505] text-white">

      {/* Background */}
      <div className="pointer-events-none fixed inset-0">
        <div className="absolute left-1/2 top-[-250px] h-[500px] w-[700px] -translate-x-1/2 rounded-full bg-blue-600/8 blur-[150px]" />

        <div
          className="absolute inset-0 opacity-[0.025]"
          style={{
            backgroundImage:
              "linear-gradient(rgba(255,255,255,0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.5) 1px, transparent 1px)",
            backgroundSize: "48px 48px",
          }}
        />
      </div>

      <div className="relative z-10 mx-auto w-full max-w-6xl px-6 py-6 lg:px-8">

        {/* Header */}
        <header className="flex items-center justify-between">

          <Link
            href="/"
            className="group flex items-center gap-3"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-zinc-800 bg-zinc-900 text-lg shadow-lg shadow-black/20 transition group-hover:border-zinc-700">
              🚀
            </div>

            <div>
              <p className="text-lg font-semibold tracking-tight">
                SQLPilot
              </p>

              <p className="text-xs text-zinc-500">
                AI Database Assistant
              </p>
            </div>
          </Link>

          <Link
            href="/"
            className="rounded-lg border border-zinc-800 bg-zinc-900/40 px-4 py-2 text-sm text-zinc-400 transition hover:border-zinc-700 hover:bg-zinc-900 hover:text-white"
          >
            ← Home
          </Link>

        </header>

        {/* Heading */}
        <section className="mx-auto mt-14 max-w-4xl text-center">

          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-blue-500/20 bg-blue-500/5 px-3.5 py-1.5 text-xs font-medium text-blue-400">
            <span className="h-1.5 w-1.5 rounded-full bg-blue-400" />
            Database Connection
          </div>

          <h1 className="text-4xl font-bold tracking-[-0.03em] sm:text-5xl">
            Connect your database
          </h1>

          <p className="mx-auto mt-4 max-w-2xl text-sm leading-6 text-zinc-500 sm:text-base">
            Connect SQLPilot to your database and start asking
            questions using natural language.
          </p>

        </section>

        {/* Saved Connections */}
        {!loadingSaved &&
          savedConnections.length > 0 && (
            <section className="mx-auto mt-10 max-w-5xl">

              <div className="mb-4 flex items-end justify-between">

                <div>
                  <h2 className="text-lg font-semibold text-white">
                    Previously connected
                  </h2>

                  <p className="mt-1 text-xs text-zinc-500">
                    Reconnect without entering your credentials again.
                  </p>
                </div>

                <div className="hidden items-center gap-2 text-xs text-zinc-600 sm:flex">
                  <span className="text-emerald-400">
                    🔒
                  </span>
                  Credentials encrypted
                </div>

              </div>

              <div className="space-y-3">

                {savedConnections.map(
                  (connection) => {
                    const database =
                      getDatabaseInfo(
                        connection.db_type
                      );

                    const isReconnecting =
                      reconnectingId ===
                      connection.id;

                    const isDeleting =
                      deletingId ===
                      connection.id;

                    return (
                      <div
                        key={connection.id}
                        className="group overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900/55 shadow-xl shadow-black/20 backdrop-blur transition hover:border-zinc-700"
                      >

                        <div className="flex flex-col gap-5 p-5 sm:flex-row sm:items-center sm:justify-between sm:p-6">

                          {/* Database info */}
                          <div className="flex min-w-0 items-center gap-4">

                            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl border border-zinc-800 bg-zinc-950 text-2xl">
                              {database.icon}
                            </div>

                            <div className="min-w-0">

                              <div className="flex flex-wrap items-center gap-2">

                                <h3 className="truncate text-sm font-semibold text-white">
                                  {connection.name}
                                </h3>

                                <span className="rounded-md border border-zinc-800 bg-zinc-950 px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-zinc-500">
                                  {database.name}
                                </span>

                              </div>

                              <p className="mt-1 text-xs text-zinc-500">
                                {connection.host}
                                <span className="mx-1.5 text-zinc-700">
                                  :
                                </span>
                                {connection.port}
                              </p>

                              <p className="mt-1 text-xs text-zinc-600">
                                {connection.username}
                              </p>

                            </div>

                          </div>

                          {/* Actions */}
                          <div className="flex items-center gap-2 sm:shrink-0">

                            <button
                              type="button"
                              onClick={() =>
                                handleReconnect(
                                  connection.id
                                )
                              }
                              disabled={
                                isReconnecting ||
                                isDeleting
                              }
                              className="group/reconnect inline-flex h-10 flex-1 items-center justify-center gap-2 rounded-lg bg-white px-4 text-xs font-semibold text-black transition hover:bg-zinc-100 disabled:cursor-not-allowed disabled:opacity-50 sm:flex-none"
                            >
                              {isReconnecting ? (
                                <>
                                  <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-zinc-400 border-t-black" />
                                  Reconnecting...
                                </>
                              ) : (
                                <>
                                  Reconnect
                                  <span className="transition-transform group-hover/reconnect:translate-x-0.5">
                                    →
                                  </span>
                                </>
                              )}
                            </button>

                            <button
                              type="button"
                              onClick={() =>
                                handleDelete(
                                  connection.id
                                )
                              }
                              disabled={
                                isDeleting ||
                                isReconnecting
                              }
                              aria-label={`Remove ${connection.name}`}
                              className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-lg border border-zinc-800 bg-zinc-950 text-zinc-600 transition hover:border-red-500/30 hover:bg-red-500/5 hover:text-red-400 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                              {isDeleting ? (
                                <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-zinc-600 border-t-red-400" />
                              ) : (
                                "×"
                              )}
                            </button>

                          </div>

                        </div>

                      </div>
                    );
                  }
                )}

              </div>

            </section>
          )}

        {/* Loading Saved Connections */}
        {loadingSaved && (
          <section className="mx-auto mt-10 max-w-5xl">

            <div className="flex items-center gap-3 rounded-2xl border border-zinc-800 bg-zinc-900/40 px-5 py-4">

              <span className="h-4 w-4 animate-spin rounded-full border-2 border-zinc-700 border-t-blue-400" />

              <span className="text-xs text-zinc-500">
                Loading saved connections...
              </span>

            </div>

          </section>
        )}

        {/* Connection Card */}
        <section
          className={`mx-auto max-w-5xl overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900/55 shadow-2xl shadow-black/40 backdrop-blur ${
            savedConnections.length > 0 || loadingSaved
              ? "mt-8"
              : "mt-10"
          }`}
        >

          {/* Card heading */}
          <div className="flex items-center justify-between border-b border-zinc-800 px-6 py-5 sm:px-8">

            <div>
              <h2 className="text-base font-semibold text-white">
                New database connection
              </h2>

              <p className="mt-1 text-xs text-zinc-500">
                Enter the credentials for the database you want to use.
              </p>
            </div>

            <div className="hidden items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-950 px-3 py-2 text-xs text-zinc-500 sm:flex">
              <span className="text-emerald-400">
                🔒
              </span>
              Secure connection
            </div>

          </div>

          <div className="p-6 sm:p-8">

            {/* Database selector */}
            <div>

              <label className="mb-3 block text-sm font-medium text-zinc-300">
                Database type
              </label>

              <div className="grid gap-3 md:grid-cols-3">

                {DATABASES.map((database) => {

                  const selected =
                    formData.db_type ===
                    database.value;

                  return (
                    <button
                      key={database.value}
                      type="button"
                      onClick={() =>
                        handleDatabaseType(
                          database.value
                        )
                      }
                      className={`group rounded-xl border p-4 text-left transition duration-200 ${
                        selected
                          ? "border-blue-500/60 bg-blue-500/8 shadow-lg shadow-blue-500/5"
                          : "border-zinc-800 bg-zinc-950/40 hover:border-zinc-700 hover:bg-zinc-900"
                      }`}
                    >

                      <div className="flex items-center justify-between">

                        <span className="text-2xl">
                          {database.icon}
                        </span>

                        {selected && (
                          <span className="flex h-5 w-5 items-center justify-center rounded-full bg-blue-500/15 text-xs font-bold text-blue-400">
                            ✓
                          </span>
                        )}

                      </div>

                      <p className="mt-4 text-sm font-semibold text-white">
                        {database.name}
                      </p>

                      <p className="mt-1 text-xs text-zinc-500">
                        {database.description}
                      </p>

                    </button>
                  );
                })}

              </div>

            </div>

            {/* Fields */}
            <div className="mt-8 grid gap-x-5 gap-y-5 md:grid-cols-2">

              {/* Host */}
              <div className="md:col-span-2">

                <label
                  htmlFor="host"
                  className="mb-2 block text-xs font-medium text-zinc-400"
                >
                  Host
                </label>

                <input
                  id="host"
                  name="host"
                  value={formData.host}
                  onChange={handleChange}
                  placeholder="localhost"
                  className="h-12 w-full rounded-xl border border-zinc-800 bg-[#080808] px-4 text-sm text-white outline-none transition placeholder:text-zinc-700 focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/10"
                />

              </div>

              {/* Port */}
              <div>

                <label
                  htmlFor="port"
                  className="mb-2 block text-xs font-medium text-zinc-400"
                >
                  Port
                </label>

                <input
                  id="port"
                  name="port"
                  type="number"
                  value={formData.port}
                  onChange={handleChange}
                  className="h-12 w-full rounded-xl border border-zinc-800 bg-[#080808] px-4 text-sm text-white outline-none transition focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/10"
                />

              </div>

              {/* Database */}
              <div>

                <label
                  htmlFor="database"
                  className="mb-2 block text-xs font-medium text-zinc-400"
                >
                  Database name
                </label>

                <input
                  id="database"
                  name="database"
                  value={formData.database}
                  onChange={handleChange}
                  placeholder="sqlpilot_demo"
                  className="h-12 w-full rounded-xl border border-zinc-800 bg-[#080808] px-4 text-sm text-white outline-none transition placeholder:text-zinc-700 focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/10"
                />

              </div>

              {/* Username */}
              <div>

                <label
                  htmlFor="username"
                  className="mb-2 block text-xs font-medium text-zinc-400"
                >
                  Username
                </label>

                <input
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  placeholder="postgres"
                  className="h-12 w-full rounded-xl border border-zinc-800 bg-[#080808] px-4 text-sm text-white outline-none transition placeholder:text-zinc-700 focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/10"
                />

              </div>

              {/* Password */}
              <div>

                <label
                  htmlFor="password"
                  className="mb-2 block text-xs font-medium text-zinc-400"
                >
                  Password
                </label>

                <input
                  id="password"
                  name="password"
                  type="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="••••••••"
                  className="h-12 w-full rounded-xl border border-zinc-800 bg-[#080808] px-4 text-sm text-white outline-none transition placeholder:text-zinc-700 focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/10"
                />

              </div>

            </div>

            {/* Action */}
            <div className="mt-8 flex flex-col gap-4 border-t border-zinc-800 pt-6 sm:flex-row sm:items-center sm:justify-between">

              <div className="flex items-center gap-2 text-xs text-zinc-600">
                <span>🔒</span>
                Credentials are encrypted and stored securely.
              </div>

              <button
                type="button"
                onClick={handleSubmit}
                disabled={loading}
                className="group inline-flex h-12 items-center justify-center gap-3 rounded-xl bg-white px-7 text-sm font-semibold text-black shadow-xl shadow-white/5 transition duration-200 hover:-translate-y-0.5 hover:bg-zinc-100 hover:shadow-white/10 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:translate-y-0"
              >

                {loading ? (
                  <>
                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-zinc-400 border-t-black" />
                    Connecting...
                  </>
                ) : (
                  <>
                    Connect Database
                    <span className="transition-transform duration-200 group-hover:translate-x-1">
                      →
                    </span>
                  </>
                )}

              </button>

            </div>

            {/* Response */}
            {response && (
              <div
                className={`mt-6 rounded-xl border p-5 ${
                  response.success
                    ? "border-emerald-500/20 bg-emerald-500/5"
                    : "border-red-500/20 bg-red-500/5"
                }`}
              >

                <div className="flex items-start gap-3">

                  <div
                    className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg ${
                      response.success
                        ? "bg-emerald-500/10 text-emerald-400"
                        : "bg-red-500/10 text-red-400"
                    }`}
                  >
                    {response.success
                      ? "✓"
                      : "!"}
                  </div>

                  <div className="min-w-0">

                    <p
                      className={`text-sm font-semibold ${
                        response.success
                          ? "text-emerald-300"
                          : "text-red-300"
                      }`}
                    >
                      {response.success
                        ? "Database connected successfully"
                        : "Connection failed"}
                    </p>

                    <p className="mt-1 text-xs leading-5 text-zinc-500">
                      {response.message}
                    </p>

                  </div>

                </div>

                {response.success && (
                  <div className="mt-5 flex flex-col gap-3 sm:flex-row">

                    <button
                      type="button"
                      onClick={() =>
                        router.push("/query")
                      }
                      className="flex-1 rounded-lg bg-emerald-500/10 px-4 py-3 text-sm font-medium text-emerald-300 transition hover:bg-emerald-500/15"
                    >
                      Open Query Workspace →
                    </button>

                  </div>
                )}

              </div>
            )}

          </div>
        </section>

        {/* Schema */}
        {response?.success &&
          response?.schema && (
            <section className="mx-auto mt-6 max-w-5xl">
              <SchemaViewer
                schema={response.schema}
              />
            </section>
          )}

        {/* Bottom note */}
        <div className="mx-auto mt-6 flex max-w-5xl items-center justify-center gap-2 pb-8 text-xs text-zinc-700">
          <span>SQLPilot</span>
          <span>•</span>
          <span>PostgreSQL</span>
          <span>•</span>
          <span>MySQL</span>
          <span>•</span>
          <span>SQLite</span>
        </div>

      </div>
    </main>
  );
}