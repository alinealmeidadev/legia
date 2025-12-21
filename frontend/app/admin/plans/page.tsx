'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import api from '@/lib/api'
import { CreditCard, Check } from 'lucide-react'

interface Plan {
  id: number
  name: string
  slug: string
  description: string
  price_monthly: number
  price_yearly: number
  max_users: number | null
  max_clients: number | null
  max_storage_gb: number
  features: string[]
  color: string
  is_active: boolean
}

export default function PlansPage() {
  const [plans, setPlans] = useState<Plan[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadPlans()
  }, [])

  const loadPlans = async () => {
    try {
      setLoading(true)
      const response = await api.get('/tenants/plans')
      setPlans(response.data)
    } catch (error) {
      console.error('Erro ao carregar planos:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(price)
  }

  const getFeatureName = (feature: string) => {
    const names: Record<string, string> = {
      leg_agents: 'Agentes de Legalização',
      whatsapp_api: 'API WhatsApp',
      email_marketing: 'Email Marketing',
      api: 'API Completa',
      white_label: 'White Label',
    }
    return names[feature] || feature
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-muted-foreground">Carregando planos...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Planos</h1>
        <p className="text-muted-foreground mt-1">
          Gerenciar planos de assinatura disponíveis
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {plans.map((plan) => (
          <Card key={plan.id} className="relative">
            <CardHeader>
              <div className="flex items-center justify-between mb-2">
                <div className="h-10 w-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: plan.color + '20' }}>
                  <CreditCard className="h-5 w-5" style={{ color: plan.color }} />
                </div>
                <Badge variant={plan.is_active ? 'default' : 'secondary'}>
                  {plan.is_active ? 'Ativo' : 'Inativo'}
                </Badge>
              </div>
              <CardTitle className="text-2xl">{plan.name}</CardTitle>
              <CardDescription>{plan.description}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-bold">{formatPrice(plan.price_monthly)}</span>
                  <span className="text-muted-foreground">/mês</span>
                </div>
                <div className="text-sm text-muted-foreground">
                  ou {formatPrice(plan.price_yearly)} /ano
                </div>
              </div>

              <div className="space-y-2 pt-4 border-t">
                <div className="text-sm">
                  <strong>Usuários:</strong> {plan.max_users || 'Ilimitado'}
                </div>
                <div className="text-sm">
                  <strong>Clientes:</strong> {plan.max_clients || 'Ilimitado'}
                </div>
                <div className="text-sm">
                  <strong>Armazenamento:</strong> {plan.max_storage_gb} GB
                </div>
              </div>

              <div className="space-y-2 pt-4 border-t">
                <div className="text-sm font-semibold mb-2">Recursos:</div>
                {plan.features.map((feature) => (
                  <div key={feature} className="flex items-center gap-2 text-sm">
                    <Check className="h-4 w-4 text-green-600" />
                    <span>{getFeatureName(feature)}</span>
                  </div>
                ))}
              </div>

              <Button className="w-full mt-4" variant="outline">
                Editar Plano
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
