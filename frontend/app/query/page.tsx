"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import QueryWorkspace from "@/components/QueryWorkspace";

export default function QueryPage() {
  const router = useRouter();

  const [checking, setChecking] = useState(true);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        const response = await api.get("/api/database/status");

        if (!response.data.connected) {
          router.replace("/connect");
          return;
        }

        setConnected(true);
      } catch (error) {
        console.error("CONNECTION STATUS ERROR:", error);
        router.replace("/connect");
      } finally {
        setChecking(false);
      }
    };

    checkConnection();
  }, [router]);

  if (checking || !connected) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-zinc-950">
        <div className="text-center">
          <div className="mx-auto mb-4 h-8 w-8 animate-spin rounded-full border-2 border-zinc-700 border-t-blue-500" />

          <p className="text-sm text-zinc-400">
            Checking database connection...
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-zinc-950">
      <QueryWorkspace />
    </main>
  );
}