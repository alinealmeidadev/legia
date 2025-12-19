'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { TenantFormDialog } from '@/components/tenant-form-dialog'
import { TenantEditDialog } from '@/components/tenant-edit-dialog'
import api from '@/lib/api'
import { Building2 } from 'lucide-react'

interface Tenant {
  id: number
  name: string
  subdomain: string
  cnpj: string
  crc?: string
  email: string
  phone?: string
  website?: string
  status: string
  plan_id: number
  created_at: string
  address_street?: string
  address_number?: string
  address_complement?: string
  address_neighborhood?: string
  address_city?: string
  address_state?: string
  address_zipcode?: string
}

export default function TenantsPage() {
  const [tenants, setTenants] = useState<Tenant[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [editingTenant, setEditingTenant] = useState<Tenant | null>(null)

  useEffect(() => {
    loadTenants()
  }, [])

  const loadTenants = async () => {
    try {
      setLoading(true)
      const response = await api.get('/tenants/')
      setTenants(response.data.tenants)
    } catch (err: any) {
      setError('Erro ao carregar tenants')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    const colors: any = {
      active: 'text-green-600 bg-green-50',
      trial: 'text-yellow-600 bg-yellow-50',
      suspended: 'text-red-600 bg-red-50',
      canceled: 'text-gray-600 bg-gray-50',
    }
    return colors[status] || 'text-gray-600 bg-gray-50'
  }

  const getStatusText = (status: string) => {
    const labels: any = {
      active: 'Ativo',
      trial: 'Trial',
      suspended: 'Suspenso',
      canceled: 'Cancelado',
    }
    return labels[status] || status
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-muted-foreground">Carregando tenants...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-red-600">{error}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Tenants</h1>
          <p className="text-muted-foreground">
            Gerenciar escritórios cadastrados na plataforma
          </p>
        </div>
        <TenantFormDialog onSuccess={loadTenants} />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Lista de Tenants</CardTitle>
          <CardDescription>
            {tenants.length} {tenants.length === 1 ? 'tenant cadastrado' : 'tenants cadastrados'}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {tenants.map((tenant) => (
              <div
                key={tenant.id}
                className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent transition-colors"
              >
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
                    <Building2 className="h-6 w-6 text-primary" />
                  </div>
                  <div>
                    <p className="font-medium">{tenant.name}</p>
                    <div className="flex gap-4 text-sm text-muted-foreground mt-1">
                      <span>{tenant.cnpj}</span>
                      <span>•</span>
                      <span>{tenant.email}</span>
                      <span>•</span>
                      <span>{tenant.subdomain}.legiaplatform.com.br</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(
                      tenant.status
                    )}`}
                  >
                    {getStatusText(tenant.status)}
                  </span>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setEditingTenant(tenant)}
                  >
                    Editar
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {editingTenant && (
        <TenantEditDialog
          tenant={editingTenant}
          open={!!editingTenant}
          onOpenChange={(open) => !open && setEditingTenant(null)}
          onSuccess={loadTenants}
        />
      )}
    </div>
  )
}
