'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { ClientFormDialog } from '@/components/client-form-dialog'
import { ClientEditDialog } from '@/components/client-edit-dialog'
import api from '@/lib/api'
import { Users } from 'lucide-react'

interface Client {
  id: number
  type: string
  name: string
  document: string
  email?: string
  phone?: string
  mobile?: string
  status: string
  company_name?: string
  trade_name?: string
  cnae_primary?: string
  state_registration?: string
  municipal_registration?: string
  address_street?: string
  address_number?: string
  address_complement?: string
  address_neighborhood?: string
  address_city?: string
  address_state?: string
  address_zipcode?: string
  created_at: string
}

export default function ClientsPage() {
  const [clients, setClients] = useState<Client[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [editingClient, setEditingClient] = useState<Client | null>(null)

  useEffect(() => {
    loadClients()
  }, [])

  const loadClients = async () => {
    try {
      setLoading(true)
      const response = await api.get('/clients/')
      setClients(response.data.clients)
    } catch (err: any) {
      setError('Erro ao carregar clientes')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    const colors: any = {
      lead: 'text-blue-600 bg-blue-50',
      active: 'text-green-600 bg-green-50',
      inactive: 'text-gray-600 bg-gray-50',
      suspended: 'text-red-600 bg-red-50',
    }
    return colors[status] || 'text-gray-600 bg-gray-50'
  }

  const getStatusText = (status: string) => {
    const labels: any = {
      lead: 'Lead',
      active: 'Ativo',
      inactive: 'Inativo',
      suspended: 'Suspenso',
    }
    return labels[status] || status
  }

  const getTypeText = (type: string) => {
    return type === 'pf' ? 'Pessoa Física' : 'Pessoa Jurídica'
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-muted-foreground">Carregando clientes...</p>
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
          <h1 className="text-3xl font-bold">Clientes</h1>
          <p className="text-muted-foreground">
            Gerenciar clientes do escritório
          </p>
        </div>
        <ClientFormDialog onSuccess={loadClients} />
      </div>

      {clients.length === 0 ? (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-12">
              <Users className="h-12 w-12 mx-auto mb-4 text-muted-foreground opacity-50" />
              <h3 className="text-lg font-medium mb-2">Nenhum cliente cadastrado</h3>
              <p className="text-muted-foreground mb-4">
                Comece adicionando seu primeiro cliente
              </p>
              <ClientFormDialog onSuccess={loadClients} />
            </div>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>Lista de Clientes</CardTitle>
            <CardDescription>
              {clients.length} {clients.length === 1 ? 'cliente cadastrado' : 'clientes cadastrados'}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {clients.map((client) => (
                <div
                  key={client.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
                      <Users className="h-6 w-6 text-primary" />
                    </div>
                    <div>
                      <p className="font-medium">{client.name}</p>
                      <div className="flex gap-4 text-sm text-muted-foreground mt-1">
                        <span>{getTypeText(client.type)}</span>
                        <span>•</span>
                        <span>{client.document}</span>
                        {client.email && (
                          <>
                            <span>•</span>
                            <span>{client.email}</span>
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(
                        client.status
                      )}`}
                    >
                      {getStatusText(client.status)}
                    </span>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setEditingClient(client)}
                    >
                      Editar
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {editingClient && (
        <ClientEditDialog
          client={editingClient}
          open={!!editingClient}
          onOpenChange={(open) => !open && setEditingClient(null)}
          onSuccess={loadClients}
        />
      )}
    </div>
  )
}
