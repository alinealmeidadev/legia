'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import api from '@/lib/api'
import { useToast } from '@/components/ui/use-toast'

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
}

interface ClientEditDialogProps {
  client: Client
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess?: () => void
}

export function ClientEditDialog({
  client,
  open,
  onOpenChange,
  onSuccess,
}: ClientEditDialogProps) {
  const [loading, setLoading] = useState(false)
  const { toast } = useToast()

  const [formData, setFormData] = useState({
    name: client.name || '',
    email: client.email || '',
    phone: client.phone || '',
    mobile: client.mobile || '',
    status: client.status || 'lead',
    company_name: client.company_name || '',
    trade_name: client.trade_name || '',
    cnae_primary: client.cnae_primary || '',
    state_registration: client.state_registration || '',
    municipal_registration: client.municipal_registration || '',
    address_street: client.address_street || '',
    address_number: client.address_number || '',
    address_complement: client.address_complement || '',
    address_neighborhood: client.address_neighborhood || '',
    address_city: client.address_city || '',
    address_state: client.address_state || '',
    address_zipcode: client.address_zipcode || '',
  })

  // Update form data when client changes
  useEffect(() => {
    setFormData({
      name: client.name || '',
      email: client.email || '',
      phone: client.phone || '',
      mobile: client.mobile || '',
      status: client.status || 'lead',
      company_name: client.company_name || '',
      trade_name: client.trade_name || '',
      cnae_primary: client.cnae_primary || '',
      state_registration: client.state_registration || '',
      municipal_registration: client.municipal_registration || '',
      address_street: client.address_street || '',
      address_number: client.address_number || '',
      address_complement: client.address_complement || '',
      address_neighborhood: client.address_neighborhood || '',
      address_city: client.address_city || '',
      address_state: client.address_state || '',
      address_zipcode: client.address_zipcode || '',
    })
  }, [client])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const data = {
        name: formData.name,
        email: formData.email || undefined,
        phone: formData.phone || undefined,
        mobile: formData.mobile || undefined,
        status: formData.status,
        company_name: client.type === 'pj' ? formData.company_name || undefined : undefined,
        trade_name: client.type === 'pj' ? formData.trade_name || undefined : undefined,
        cnae_primary: client.type === 'pj' ? formData.cnae_primary || undefined : undefined,
        state_registration: client.type === 'pj' ? formData.state_registration || undefined : undefined,
        municipal_registration: client.type === 'pj' ? formData.municipal_registration || undefined : undefined,
        address_street: formData.address_street || undefined,
        address_number: formData.address_number || undefined,
        address_complement: formData.address_complement || undefined,
        address_neighborhood: formData.address_neighborhood || undefined,
        address_city: formData.address_city || undefined,
        address_state: formData.address_state || undefined,
        address_zipcode: formData.address_zipcode || undefined,
      }

      await api.patch(`/clients/${client.id}`, data)

      toast({
        title: 'Sucesso!',
        description: 'Cliente atualizado com sucesso.',
      })

      onOpenChange(false)

      if (onSuccess) {
        onSuccess()
      }
    } catch (error: any) {
      console.error('Erro ao atualizar cliente:', error)
      toast({
        variant: 'destructive',
        title: 'Erro',
        description: error.response?.data?.detail || 'Erro ao atualizar cliente.',
      })
    } finally {
      setLoading(false)
    }
  }

  const formatCEP = (value: string) => {
    const numbers = value.replace(/\D/g, '')
    if (numbers.length <= 8) {
      return numbers.replace(/^(\d{5})(\d)/, '$1-$2')
    }
    return value
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Editar Cliente</DialogTitle>
          <DialogDescription>
            Atualize as informações do cliente {client.name}
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            {/* Informações Básicas */}
            <div className="grid gap-2">
              <Label htmlFor="name">
                {client.type === 'pf' ? 'Nome Completo *' : 'Razão Social *'}
              </Label>
              <Input
                id="name"
                required
                value={formData.name}
                onChange={(e) =>
                  setFormData({ ...formData, name: e.target.value })
                }
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="grid gap-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                />
              </div>

              <div className="grid gap-2">
                <Label htmlFor="status">Status *</Label>
                <Select
                  value={formData.status}
                  onValueChange={(value) =>
                    setFormData({ ...formData, status: value })
                  }
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="lead">Lead</SelectItem>
                    <SelectItem value="active">Ativo</SelectItem>
                    <SelectItem value="inactive">Inativo</SelectItem>
                    <SelectItem value="suspended">Suspenso</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="grid gap-2">
                <Label htmlFor="phone">Telefone</Label>
                <Input
                  id="phone"
                  value={formData.phone}
                  onChange={(e) =>
                    setFormData({ ...formData, phone: e.target.value })
                  }
                />
              </div>

              <div className="grid gap-2">
                <Label htmlFor="mobile">Celular</Label>
                <Input
                  id="mobile"
                  value={formData.mobile}
                  onChange={(e) =>
                    setFormData({ ...formData, mobile: e.target.value })
                  }
                />
              </div>
            </div>

            {/* Dados PJ */}
            {client.type === 'pj' && (
              <div className="border-t pt-4 mt-2">
                <h3 className="text-sm font-medium mb-3">Dados da Empresa</h3>

                <div className="grid gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="trade_name">Nome Fantasia</Label>
                    <Input
                      id="trade_name"
                      value={formData.trade_name}
                      onChange={(e) =>
                        setFormData({ ...formData, trade_name: e.target.value })
                      }
                    />
                  </div>

                  <div className="grid gap-2">
                    <Label htmlFor="company_name">Razão Social Completa</Label>
                    <Input
                      id="company_name"
                      value={formData.company_name}
                      onChange={(e) =>
                        setFormData({ ...formData, company_name: e.target.value })
                      }
                    />
                  </div>

                  <div className="grid grid-cols-3 gap-4">
                    <div className="grid gap-2">
                      <Label htmlFor="cnae_primary">CNAE Principal</Label>
                      <Input
                        id="cnae_primary"
                        value={formData.cnae_primary}
                        onChange={(e) =>
                          setFormData({
                            ...formData,
                            cnae_primary: e.target.value,
                          })
                        }
                      />
                    </div>

                    <div className="grid gap-2">
                      <Label htmlFor="state_registration">Inscrição Estadual</Label>
                      <Input
                        id="state_registration"
                        value={formData.state_registration}
                        onChange={(e) =>
                          setFormData({
                            ...formData,
                            state_registration: e.target.value,
                          })
                        }
                      />
                    </div>

                    <div className="grid gap-2">
                      <Label htmlFor="municipal_registration">
                        Inscrição Municipal
                      </Label>
                      <Input
                        id="municipal_registration"
                        value={formData.municipal_registration}
                        onChange={(e) =>
                          setFormData({
                            ...formData,
                            municipal_registration: e.target.value,
                          })
                        }
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Endereço */}
            <div className="border-t pt-4 mt-2">
              <h3 className="text-sm font-medium mb-3">Endereço</h3>

              <div className="grid gap-4">
                <div className="grid grid-cols-3 gap-4">
                  <div className="col-span-2 grid gap-2">
                    <Label htmlFor="address_street">Rua</Label>
                    <Input
                      id="address_street"
                      value={formData.address_street}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          address_street: e.target.value,
                        })
                      }
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="address_number">Número</Label>
                    <Input
                      id="address_number"
                      value={formData.address_number}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          address_number: e.target.value,
                        })
                      }
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="address_complement">Complemento</Label>
                    <Input
                      id="address_complement"
                      value={formData.address_complement}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          address_complement: e.target.value,
                        })
                      }
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="address_neighborhood">Bairro</Label>
                    <Input
                      id="address_neighborhood"
                      value={formData.address_neighborhood}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          address_neighborhood: e.target.value,
                        })
                      }
                    />
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="address_city">Cidade</Label>
                    <Input
                      id="address_city"
                      value={formData.address_city}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          address_city: e.target.value,
                        })
                      }
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="address_state">Estado</Label>
                    <Input
                      id="address_state"
                      value={formData.address_state}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          address_state: e.target.value.toUpperCase().slice(0, 2),
                        })
                      }
                      placeholder="SP"
                      maxLength={2}
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="address_zipcode">CEP</Label>
                    <Input
                      id="address_zipcode"
                      value={formData.address_zipcode}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          address_zipcode: formatCEP(e.target.value),
                        })
                      }
                      placeholder="00000-000"
                      maxLength={9}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={loading}
            >
              Cancelar
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? 'Salvando...' : 'Salvar Alterações'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
