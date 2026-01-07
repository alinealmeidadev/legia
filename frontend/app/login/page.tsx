'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { authService } from '@/lib/auth'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [tenantId, setTenantId] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await authService.login(
        { email, password },
        tenantId ? parseInt(tenantId) : undefined
      )

      // Salvar no localStorage
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('refresh_token', response.refresh_token)
      localStorage.setItem('user', JSON.stringify(response.user))

      // Redirecionar baseado no tipo de usuário
      if (response.user.user_type === 'legia_user') {
        router.push('/admin')
      } else {
        router.push('/tenant')
      }
    } catch (err: any) {
      console.error('Login error:', err)
      setError(err.response?.data?.detail || 'Erro ao fazer login. Verifique suas credenciais.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-blue-100 p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <div className="flex items-center justify-center mb-4">
            <div className="text-4xl font-bold text-primary">LEGIA</div>
          </div>
          <CardTitle className="text-2xl text-center">Bem-vindo</CardTitle>
          <CardDescription className="text-center">
            Entre com suas credenciais para acessar a plataforma
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="seu@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={loading}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Senha</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="tenantId">
                ID do Tenant <span className="text-xs text-muted-foreground">(opcional - para usuários de escritório)</span>
              </Label>
              <Input
                id="tenantId"
                type="number"
                placeholder="1"
                value={tenantId}
                onChange={(e) => setTenantId(e.target.value)}
                disabled={loading}
              />
            </div>

            {error && (
              <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md">
                {error}
              </div>
            )}

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Entrando...' : 'Entrar'}
            </Button>

            {/* CREDENCIAIS REMOVIDAS POR SEGURANÇA
                 Em desenvolvimento, consulte a documentação ou .env */}
            {process.env.NODE_ENV === 'development' && (
              <div className="text-xs text-center text-muted-foreground mt-4">
                <p className="text-yellow-600">⚠️ Ambiente de desenvolvimento</p>
                <p>Consulte CLAUDE.md para credenciais de teste</p>
              </div>
            )}
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
