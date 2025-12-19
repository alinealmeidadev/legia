'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Building2, Users, CreditCard, TrendingUp } from 'lucide-react'

export default function AdminDashboard() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Dashboard Super Admin</h1>
        <p className="text-muted-foreground">
          Visão geral da plataforma LEGIA
        </p>
      </div>

      {/* Métricas */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Total de Tenants
            </CardTitle>
            <Building2 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2</div>
            <p className="text-xs text-muted-foreground">
              +1 este mês
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Tenants Ativos
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1</div>
            <p className="text-xs text-muted-foreground">
              50% de conversão
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Receita Mensal
            </CardTitle>
            <CreditCard className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">R$ 597</div>
            <p className="text-xs text-muted-foreground">
              1 assinatura ativa
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Usuários Totais
            </CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">2</div>
            <p className="text-xs text-muted-foreground">
              Todos os tenants
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Tenants Recentes */}
      <Card>
        <CardHeader>
          <CardTitle>Tenants Recentes</CardTitle>
          <CardDescription>
            Últimos escritórios cadastrados na plataforma
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 border rounded-lg">
              <div>
                <p className="font-medium">Escritório ABC Contabilidade</p>
                <p className="text-sm text-muted-foreground">12.345.678/0001-90</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-medium text-green-600">Ativo</p>
                <p className="text-xs text-muted-foreground">Plano: Pro</p>
              </div>
            </div>

            <div className="flex items-center justify-between p-4 border rounded-lg">
              <div>
                <p className="font-medium">Escritório XYZ Assessoria</p>
                <p className="text-sm text-muted-foreground">98.765.432/0001-10</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-medium text-yellow-600">Trial</p>
                <p className="text-xs text-muted-foreground">Plano: Pro</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
