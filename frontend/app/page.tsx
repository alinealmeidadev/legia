'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { authService } from '@/lib/auth'

export default function HomePage() {
  const router = useRouter()

  useEffect(() => {
    if (authService.isAuthenticated()) {
      const user = authService.getCurrentUser()

      if (user?.user_type === 'legia_user') {
        router.push('/admin')
      } else {
        router.push('/tenant')
      }
    } else {
      router.push('/login')
    }
  }, [router])

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-2">LEGIA PLATFORM</h1>
        <p className="text-muted-foreground">Carregando...</p>
      </div>
    </div>
  )
}
