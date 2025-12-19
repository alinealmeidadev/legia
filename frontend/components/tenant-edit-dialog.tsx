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
  address_street?: string
  address_number?: string
  address_complement?: string
  address_neighborhood?: string
  address_city?: string
  address_state?: string
  address_zipcode?: string
}

interface TenantEditDialogProps {
  tenant: Tenant
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess?: () => void
}

export function TenantEditDialog({
  tenant,
  open,
  onOpenChange,
  onSuccess,
}: TenantEditDialogProps) {
  const [loading, setLoading] = useState(false)
  const { toast } = useToast()

  const [formData, setFormData] = useState({
    name: tenant.name || '',
    email: tenant.email || '',
    phone: tenant.phone || '',
    website: tenant.website || '',
    crc: tenant.crc || '',
    status: tenant.status || 'active',
    plan_id: tenant.plan_id?.toString() || '1',
    address_street: tenant.address_street || '',
    address_number: tenant.address_number || '',
    address_complement: tenant.address_complement || '',
    address_neighborhood: tenant.address_neighborhood || '',
    address_city: tenant.address_city || '',
    address_state: tenant.address_state || '',
    address_zipcode: tenant.address_zipcode || '',
  })

  // Update form data when tenant changes
  useEffect(() => {
    setFormData({
      name: tenant.name || '',
      email: tenant.email || '',
      phone: tenant.phone || '',
      website: tenant.website || '',
      crc: tenant.crc || '',
      status: tenant.status || 'active',
      plan_id: tenant.plan_id?.toString() || '1',
      address_street: tenant.address_street || '',
      address_number: tenant.address_number || '',
      address_complement: tenant.address_complement || '',
      address_neighborhood: tenant.address_neighborhood || '',
      address_city: tenant.address_city || '',
      address_state: tenant.address_state || '',
      address_zipcode: tenant.address_zipcode || '',
    })
  }, [tenant])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const data = {
        name: formData.name,
        email: formData.email,
        phone: formData.phone || undefined,
        website: formData.website || undefined,
        crc: formData.crc || undefined,
        status: formData.status,
        plan_id: parseInt(formData.plan_id),
        address_street: formData.address_street || undefined,
        address_number: formData.address_number || undefined,
        address_complement: formData.address_complement || undefined,
        address_neighborhood: formData.address_neighborhood || undefined,
        address_city: formData.address_city || undefined,
        address_state: formData.address_state || undefined,
        address_zipcode: formData.address_zipcode || undefined,
      }

      await api.patch(`/tenants/${tenant.id}`, data)

      toast({
        title: 'Sucesso!',
        description: 'Tenant atualizado com sucesso.',
      })

      onOpenChange(false)

      if (onSuccess) {
        onSuccess()
      }
    } catch (error: any) {
      console.error('Erro ao atualizar tenant:', error)
      toast({
        variant: 'destructive',
        title: 'Erro',
        description: error.response?.data?.detail || 'Erro ao atualizar tenant.',
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
          <DialogTitle>Editar Tenant</DialogTitle>
          <DialogDescription>
            Atualize as informações do tenant {tenant.name}
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            {/* Informações Básicas */}
            <div className="grid gap-2">
              <Label htmlFor="name">Nome do Escritório *</Label>
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
                <Label htmlFor="email">Email *</Label>
                <Input
                  id="email"
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                />
              </div>

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
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="grid gap-2">
                <Label htmlFor="crc">CRC</Label>
                <Input
                  id="crc"
                  value={formData.crc}
                  onChange={(e) =>
                    setFormData({ ...formData, crc: e.target.value })
                  }
                />
              </div>

              <div className="grid gap-2">
                <Label htmlFor="website">Website</Label>
                <Input
                  id="website"
                  value={formData.website}
                  onChange={(e) =>
                    setFormData({ ...formData, website: e.target.value })
                  }
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="grid gap-2">
                <Label htmlFor="plan_id">Plano *</Label>
                <Select
                  value={formData.plan_id}
                  onValueChange={(value) =>
                    setFormData({ ...formData, plan_id: value })
                  }
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1">Básico - R$ 97,00/mês</SelectItem>
                    <SelectItem value="2">Pro - R$ 597,00/mês</SelectItem>
                    <SelectItem value="3">Enterprise - R$ 1.997,00/mês</SelectItem>
                  </SelectContent>
                </Select>
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
                    <SelectItem value="trial">Trial</SelectItem>
                    <SelectItem value="active">Ativo</SelectItem>
                    <SelectItem value="suspended">Suspenso</SelectItem>
                    <SelectItem value="canceled">Cancelado</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

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
