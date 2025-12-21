'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { authService } from '@/lib/auth'
import {
  LayoutDashboard,
  Building2,
  Users,
  CreditCard,
  Settings,
  LogOut,
  FileText,
  Folder,
  MessageSquare,
  FileSignature,
  Rocket,
  HeadphonesIcon,
} from 'lucide-react'

interface NavItem {
  title: string
  href: string
  icon: any
}

const adminNavItems: NavItem[] = [
  { title: 'Dashboard', href: '/admin', icon: LayoutDashboard },
  { title: 'Tenants', href: '/admin/tenants', icon: Building2 },
  { title: 'Planos', href: '/admin/plans', icon: CreditCard },
  { title: 'Usuários', href: '/admin/users', icon: Users },
  { title: 'Suporte', href: '/admin/support', icon: HeadphonesIcon },
  { title: 'Configurações', href: '/admin/settings', icon: Settings },
]

const tenantNavItems: NavItem[] = [
  { title: 'Dashboard', href: '/tenant', icon: LayoutDashboard },
  { title: 'Automação', href: '/tenant/automation', icon: Rocket },
  { title: 'Clientes', href: '/tenant/clients', icon: Users },
  { title: 'Processos', href: '/tenant/processes', icon: Folder },
  { title: 'Contratos', href: '/tenant/contracts', icon: FileSignature },
  { title: 'Documentos', href: '/tenant/documents', icon: FileText },
  { title: 'Comunicações', href: '/tenant/communications', icon: MessageSquare },
  { title: 'Configurações', href: '/tenant/settings', icon: Settings },
]

export function Sidebar({ userType }: { userType: 'admin' | 'tenant' }) {
  const pathname = usePathname()
  const router = useRouter()
  const [user, setUser] = useState<any>(null)
  const navItems = userType === 'admin' ? adminNavItems : tenantNavItems

  useEffect(() => {
    // Carrega o usuário apenas no cliente (depois da hidratação)
    setUser(authService.getCurrentUser())
  }, [])

  const handleLogout = async () => {
    await authService.logout()
    router.push('/login')
  }

  return (
    <div className="flex h-full w-64 flex-col gap-2 bg-card border-r">
      {/* Logo */}
      <div className="flex h-16 items-center border-b px-6">
        <h1 className="text-xl font-bold text-primary">LEGIA</h1>
      </div>

      {/* User Info */}
      <div className="px-4 py-3 border-b">
        <p className="text-sm font-medium">{user?.name}</p>
        <p className="text-xs text-muted-foreground">{user?.email}</p>
        {user?.tenant_name && (
          <p className="text-xs text-muted-foreground mt-1">
            {user.tenant_name}
          </p>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3 py-2">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname === item.href

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors',
                isActive
                  ? 'bg-primary text-primary-foreground'
                  : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
              )}
            >
              <Icon className="h-4 w-4" />
              {item.title}
            </Link>
          )
        })}
      </nav>

      {/* Logout */}
      <div className="px-3 py-4 border-t">
        <Button
          variant="ghost"
          className="w-full justify-start"
          onClick={handleLogout}
        >
          <LogOut className="mr-2 h-4 w-4" />
          Sair
        </Button>
      </div>
    </div>
  )
}
