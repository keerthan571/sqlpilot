interface SchemaViewerProps {
  schema: Record<string, any>;
}

export default function SchemaViewer({
  schema,
}: SchemaViewerProps) {
  return (
    <div className="mt-8 rounded-lg border border-zinc-800 bg-zinc-900 p-6">
      <h2 className="mb-4 text-xl font-bold text-white">
        Database Schema
      </h2>

      {Object.entries(schema).map(([table, details]) => (
        <div key={table} className="mb-6">

          <h3 className="text-lg font-semibold text-blue-400">
            📁 {table}
          </h3>

          <ul className="ml-6 mt-2 space-y-1">

            {(details as any).columns.map(
              (column: any) => (
                <li
                  key={column.name}
                  className="text-gray-300"
                >
                  • {column.name}
                  <span className="ml-2 text-gray-500">
                    ({column.type})
                  </span>
                </li>
              )
            )}

          </ul>
        </div>
      ))}
    </div>
  );
}