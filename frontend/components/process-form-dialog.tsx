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
  DialogTrigger,
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
import { useToast } from '@/components/ui/use-toast'
import api from '@/lib/api'
import { Plus, Loader2 } from 'lucide-react'

interface Client {
  id: number
  name: string
  document: string
}

export function ProcessFormDialog({ onSuccess }: { onSuccess: () => void }) {
  const [open, setOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const [clients, setClients] = useState<Client[]>([])
  const { toast } = useToast()

  const [formData, setFormData] = useState({
    client_id: '',
    process_type: 'abertura',
    title: '',
    description: '',
    priority: 'normal',
    estimated_days: '30',
  })

  useEffect(() => {
    if (open) {
      loadClients()
    }
  }, [open])

  const loadClients = async () => {
    try {
      const response = await api.get('/clients/?limit=100')
      setClients(response.data.clients)
    } catch (err) {
      console.error('Erro ao carregar clientes:', err)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      await api.post('/processes/', {
        ...formData,
        client_id: parseInt(formData.client_id),
        estimated_days: parseInt(formData.estimated_days),
      })

      toast({
        title: 'Sucesso!',
        description: 'Processo criado com sucesso.',
      })

      setOpen(false)
      resetForm()
      onSuccess()
    } catch (error: any) {
      toast({
        title: 'Erro',
        description: error.response?.data?.detail || 'Erro ao criar processo',
        variant: 'destructive',
      })
    } finally {
      setLoading(false)
    }
  }

  const resetForm = () => {
    setFormData({
      client_id: '',
      process_type: 'abertura',
      title: '',
      description: '',
      priority: 'normal',
      estimated_days: '30',
    })
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Novo Processo
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[600px]">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>Novo Processo</DialogTitle>
            <DialogDescription>
              Crie um novo processo de legalização
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 py-4">
            {/* Cliente */}
            <div className="grid gap-2">
              <Label htmlFor="client_id">
                Cliente *
              </Label>
              <Select
                value={formData.client_id}
                onValueChange={(value) =>
                  setFormData({ ...formData, client_id: value })
                }
                required
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecione o cliente" />
                </SelectTrigger>
                <SelectContent>
                  {clients.map((client) => (
                    <SelectItem key={client.id} value={client.id.toString()}>
                      {client.name} - {client.document}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Tipo de Processo */}
            <div className="grid gap-2">
              <Label htmlFor="process_type">Tipo de Processo *</Label>
              <Select
                value={formData.process_type}
                onValueChange={(value) =>
                  setFormData({ ...formData, process_type: value })
                }
                required
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="abertura">Abertura de Empresa</SelectItem>
                  <SelectItem value="alteracao">Alteração Contratual</SelectItem>
                  <SelectItem value="regularizacao">Regularização</SelectItem>
                  <SelectItem value="encerramento">Encerramento</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Título */}
            <div className="grid gap-2">
              <Label htmlFor="title">Título do Processo *</Label>
              <Input
                id="title"
                value={formData.title}
                onChange={(e) =>
                  setFormData({ ...formData, title: e.target.value })
                }
                placeholder="Ex: Abertura de LTDA - Consultoria TI"
                required
                maxLength={200}
              />
            </div>

            {/* Descrição */}
            <div className="grid gap-2">
              <Label htmlFor="description">Descrição</Label>
              <textarea
                id="description"
                className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                value={formData.description}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
                placeholder="Descreva os detalhes do processo..."
                rows={3}
              />
            </div>

            {/* Prioridade e Prazo */}
            <div className="grid grid-cols-2 gap-4">
              <div className="grid gap-2">
                <Label htmlFor="priority">Prioridade</Label>
                <Select
                  value={formData.priority}
                  onValueChange={(value) =>
                    setFormData({ ...formData, priority: value })
                  }
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="baixa">Baixa</SelectItem>
                    <SelectItem value="normal">Normal</SelectItem>
                    <SelectItem value="alta">Alta</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="grid gap-2">
                <Label htmlFor="estimated_days">Prazo (dias)</Label>
                <Input
                  id="estimated_days"
                  type="number"
                  min="1"
                  max="365"
                  value={formData.estimated_days}
                  onChange={(e) =>
                    setFormData({ ...formData, estimated_days: e.target.value })
                  }
                  required
                />
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => setOpen(false)}
              disabled={loading}
            >
              Cancelar
            </Button>
            <Button type="submit" disabled={loading}>
              {loading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Criar Processo
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
