'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { authService } from '@/lib/auth'
import { Sidebar } from '@/components/sidebar'

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/login')
      return
    }

    if (!authService.isSuperAdmin()) {
      router.push('/tenant')
    }
  }, [router])

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar userType="admin" />
      <main className="flex-1 overflow-y-auto bg-background p-6">
        {children}
      </main>
    </div>
  )
}
