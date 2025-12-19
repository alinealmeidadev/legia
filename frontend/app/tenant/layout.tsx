'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { authService } from '@/lib/auth'
import { Sidebar } from '@/components/sidebar'
import { ChatWidget } from '@/components/chat-widget'

export default function TenantLayout({
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

    if (!authService.isTenantUser()) {
      router.push('/admin')
    }
  }, [router])

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar userType="tenant" />
      <main className="flex-1 overflow-y-auto bg-background p-6">
        {children}
      </main>
      <ChatWidget />
    </div>
  )
}
