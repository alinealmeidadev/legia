"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/lib/auth";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    const workflowId = searchParams.get("workflow");

    if (!workflowId) {
      setError("Workflow não informado");
      return;
    }

    const loadWorkflow = async () => {
      try {
        setLoading(true);
        const res = await api.get(`/workflows/${workflowId}`);

        if (!res.data?.id || !res.data?.stages) {
          throw new Error("Workflow inválido");
        }

        setWorkflow(res.data);
      } catch (err: any) {
        console.error(err);
        setError(
          err.response?.data?.detail ||
            err.message ||
            "Erro ao carregar workflow"
        );
      } finally {
        setLoading(false);
      }
    };

    loadWorkflow();
  }, []);
}
