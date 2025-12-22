"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/lib/auth";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    // Verificar se já está autenticado
    if (authService.isAuthenticated()) {
      const user = authService.getCurrentUser();

      if (user) {
        // Redirecionar para dashboard apropriado
        if (user.user_type === 'legia_user' || user.role === 'superadmin') {
          router.push('/admin');
        } else {
          router.push('/tenant');
        }
      } else {
        // Token existe mas user não, ir para login
        router.push('/login');
      }
    } else {
      // Não autenticado, ir para login
      router.push('/login');
    }
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
    </div>
  );
}
