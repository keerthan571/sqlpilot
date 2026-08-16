import Link from "next/link";

export default function Home() {
  return (
    <main className="relative min-h-screen overflow-hidden bg-[#050505] text-white">
      {/* Background */}
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute left-1/2 top-[-180px] h-[500px] w-[700px] -translate-x-1/2 rounded-full bg-blue-600/10 blur-[140px]" />
        <div className="absolute bottom-[-220px] left-[-120px] h-[450px] w-[450px] rounded-full bg-indigo-600/10 blur-[140px]" />

        <div
          className="absolute inset-0 opacity-[0.035]"
          style={{
            backgroundImage:
              "linear-gradient(rgba(255,255,255,0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.5) 1px, transparent 1px)",
            backgroundSize: "48px 48px",
          }}
        />
      </div>

      {/* Navigation */}
      <nav className="relative z-10 mx-auto flex max-w-7xl items-center justify-between px-6 py-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-zinc-700 bg-zinc-900 text-lg shadow-lg shadow-black/30">
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
        </div>

        <div className="flex items-center gap-2 rounded-full border border-zinc-800 bg-zinc-900/70 px-3 py-1.5 backdrop-blur">
          <span className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_10px_rgba(52,211,153,0.7)]" />

          <span className="text-xs font-medium text-zinc-400">
            System Ready
          </span>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative z-10 mx-auto flex min-h-[calc(100vh-88px)] max-w-7xl items-center justify-center px-6 pb-16 pt-8 lg:px-8">
        <div className="w-full max-w-5xl text-center">

          {/* Badge */}
          <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-zinc-800 bg-zinc-900/70 px-4 py-2 text-sm text-zinc-400 shadow-xl shadow-black/20 backdrop-blur">
            <span className="text-blue-400">✦</span>
            Natural language → safe SQL
          </div>

          {/* Heading */}
          <h1 className="mx-auto max-w-4xl text-5xl font-bold tracking-[-0.04em] sm:text-6xl lg:text-7xl">
            Talk to your database

            <span className="block bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-400 bg-clip-text text-transparent">
              like a human.
            </span>
          </h1>

          {/* Description */}
          <p className="mx-auto mt-7 max-w-2xl text-base leading-7 text-zinc-400 sm:text-lg">
            Ask questions in plain English. SQLPilot understands your
            database schema, generates SQL, validates it for safety,
            and returns the results instantly.
          </p>

          {/* CTA */}
          <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link
              href="/connect"
              className="group inline-flex min-w-[220px] items-center justify-center gap-3 rounded-xl bg-white px-6 py-3.5 text-sm font-semibold text-black shadow-xl shadow-white/10 transition duration-200 hover:-translate-y-0.5 hover:bg-zinc-100 hover:shadow-white/20"
            >
              <span>Connect to Database</span>

              <span className="transition-transform duration-200 group-hover:translate-x-1">
                →
              </span>
            </Link>
          </div>

          <p className="mt-4 text-xs text-zinc-600">
            PostgreSQL • MySQL • SQLite
          </p>

          {/* Product Preview */}
          <div className="mx-auto mt-16 max-w-4xl">
            <div className="rounded-2xl border border-zinc-800 bg-zinc-900/60 p-2 shadow-2xl shadow-black/50 backdrop-blur">
              <div className="rounded-xl border border-zinc-800/80 bg-[#080808]">

                {/* Window header */}
                <div className="flex items-center justify-between border-b border-zinc-800 px-4 py-3">
                  <div className="flex items-center gap-1.5">
                    <span className="h-2.5 w-2.5 rounded-full bg-red-400/70" />
                    <span className="h-2.5 w-2.5 rounded-full bg-yellow-400/70" />
                    <span className="h-2.5 w-2.5 rounded-full bg-green-400/70" />
                  </div>

                  <div className="hidden items-center gap-2 rounded-md border border-zinc-800 bg-zinc-900 px-3 py-1 text-xs text-zinc-500 sm:flex">
                    <span className="h-1.5 w-1.5 rounded-full bg-blue-400" />
                    SQLPilot Preview
                  </div>

                  <div className="w-12" />
                </div>

                {/* Query preview */}
                <div className="p-5 text-left sm:p-7">

                  <div className="mb-5 flex items-center justify-between">
                    <div>
                      <p className="text-xs font-medium uppercase tracking-wider text-zinc-600">
                        Ask your database
                      </p>

                      <p className="mt-1 text-sm text-zinc-300">
                        Show customers with their total order amount
                      </p>
                    </div>
                  </div>

                  {/* Generated SQL */}
                  <div className="rounded-xl border border-zinc-800 bg-black/70 p-4">
                    <div className="mb-3 flex items-center justify-between">
                      <span className="text-xs font-medium text-zinc-600">
                        Generated SQL
                      </span>

                      <span className="rounded-md border border-emerald-500/20 bg-emerald-500/5 px-2 py-1 text-[10px] font-medium text-emerald-400">
                        VALIDATED
                      </span>
                    </div>

                    <code className="block overflow-x-auto whitespace-nowrap font-mono text-xs leading-6 text-zinc-400 sm:text-sm">
                      <span className="text-purple-400">
                        SELECT
                      </span>{" "}
                      c.name,{" "}
                      <span className="text-blue-400">
                        SUM
                      </span>
                      (o.amount)
                      <br />

                      <span className="text-purple-400">
                        FROM
                      </span>{" "}
                      customers c{" "}

                      <span className="text-purple-400">
                        JOIN
                      </span>{" "}
                      orders o
                      <br />

                      <span className="text-purple-400">
                        ON
                      </span>{" "}
                      c.id = o.customer_id
                    </code>
                  </div>

                  {/* Result preview */}
                  <div className="mt-4 grid gap-3 sm:grid-cols-2">

                    <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-4">
                      <p className="text-xs text-zinc-600">
                        Customer
                      </p>

                      <p className="mt-1 text-sm font-medium text-zinc-300">
                        John Doe
                      </p>

                      <p className="mt-2 text-xs text-zinc-600">
                        Total orders
                      </p>

                      <p className="mt-1 text-lg font-semibold text-white">
                        $1,500
                      </p>
                    </div>

                    <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-4">
                      <p className="text-xs text-zinc-600">
                        Customer
                      </p>

                      <p className="mt-1 text-sm font-medium text-zinc-300">
                        Alice
                      </p>

                      <p className="mt-2 text-xs text-zinc-600">
                        Total orders
                      </p>

                      <p className="mt-1 text-lg font-semibold text-white">
                        $1,200
                      </p>
                    </div>

                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Feature cards */}
          <div className="mx-auto mt-8 grid max-w-4xl gap-3 text-left sm:grid-cols-3">

            {/* Feature 1 */}
            <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 backdrop-blur">
              <div className="mb-3 flex h-9 w-9 items-center justify-center rounded-lg border border-zinc-800 bg-zinc-900">
                ⚡
              </div>

              <h3 className="text-sm font-semibold text-zinc-200">
                Natural Language
              </h3>

              <p className="mt-1 text-xs leading-5 text-zinc-500">
                Ask database questions without writing SQL manually.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 backdrop-blur">
              <div className="mb-3 flex h-9 w-9 items-center justify-center rounded-lg border border-zinc-800 bg-zinc-900">
                🔐
              </div>

              <h3 className="text-sm font-semibold text-zinc-200">
                Safety First
              </h3>

              <p className="mt-1 text-xs leading-5 text-zinc-500">
                Generated SQL is validated before it reaches your database.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4 backdrop-blur">
              <div className="mb-3 flex h-9 w-9 items-center justify-center rounded-lg border border-zinc-800 bg-zinc-900">
                📊
              </div>

              <h3 className="text-sm font-semibold text-zinc-200">
                Instant Results
              </h3>

              <p className="mt-1 text-xs leading-5 text-zinc-500">
                Execute valid queries and explore the results immediately.
              </p>
            </div>

          </div>

        </div>
      </section>
    </main>
  );
}