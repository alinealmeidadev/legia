'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Checkbox } from '@/components/ui/checkbox'
import { Label } from '@/components/ui/label'
import { useToast } from '@/components/ui/use-toast'
import api from '@/lib/api'
import {
  FileText,
  MapPin,
  Users,
  DollarSign,
  Briefcase,
  Building,
  XCircle
} from 'lucide-react'

type ContractOption = {
  id: string
  label: string
  description: string
}

type ContractType = {
  id: string
  title: string
  description: string
  icon: any
  options: ContractOption[]
}

export default function ContractsPage() {
  const router = useRouter()
  const { toast } = useToast()

  const [selectedType, setSelectedType] = useState<ContractType | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [selectedAlterations, setSelectedAlterations] = useState<string[]>([])
  const [loading, setLoading] = useState(false)

  const contractTypes: ContractType[] = [
    {
      id: 'alteracao',
      title: 'Alteração Contratual',
      description: 'Alterações diversas no contrato social',
      icon: Users,
      options: [
        { id: 'endereco', label: 'Alteração de Endereço', description: 'Mudança do endereço da sede social' },
        { id: 'socios', label: 'Alteração de Quadro Societário', description: 'Inclusão, exclusão ou alteração de sócios' },
        { id: 'capital', label: 'Alteração de Capital Social', description: 'Aumento ou redução do capital social' },
        { id: 'atividade', label: 'Alteração de Atividade', description: 'Inclusão ou exclusão de CNAEs' },
        { id: 'nome', label: 'Alteração de Nome Empresarial', description: 'Mudança da razão social ou nome fantasia' },
        { id: 'administracao', label: 'Alteração de Administração', description: 'Mudança de administradores/diretores' }
      ]
    },
    {
      id: 'abertura',
      title: 'Abertura de Empresa',
      description: 'Constituir nova empresa',
      icon: Building,
      options: [] // Não tem múltipla escolha
    },
    {
      id: 'distrato',
      title: 'Distrato Social (Encerramento)',
      description: 'Encerramento da empresa',
      icon: XCircle,
      options: [] // Não tem múltipla escolha
    }
  ]

  const handleCardClick = (type: ContractType) => {
    setSelectedType(type)
    setSelectedAlterations([])
    setIsModalOpen(true)
  }

  const handleCheckboxChange = (optionId: string, checked: boolean) => {
    if (checked) {
      setSelectedAlterations([...selectedAlterations, optionId])
    } else {
      setSelectedAlterations(selectedAlterations.filter(x => x !== optionId))
    }
  }

  const handleConfirm = async () => {
    if (!selectedType) return

    // Validar se precisa de seleções
    if (selectedType.options.length > 0 && selectedAlterations.length === 0) {
      toast({
        title: 'Atenção',
        description: 'Selecione pelo menos uma alteração',
        variant: 'destructive'
      })
      return
    }

    try {
      setLoading(true)

      // ETAPA 1: CRIAR PROCESSO
      const processResponse = await api.post('/processes/', {
        process_type: selectedType.id,
        title: selectedType.title,
        description: selectedType.options.length > 0
          ? `Alterações: ${selectedAlterations.join(', ')}`
          : selectedType.description,
        client_id: 1, // TODO: Substituir por cliente real
        alteration_types: selectedAlterations.length > 0 ? selectedAlterations : undefined,
        priority: 'normal',
        status: 'aguardando'
      })

      // VALIDAÇÃO 1: Processo criado?
      if (!processResponse?.data?.id) {
        throw new Error('Processo não foi criado')
      }

      const processId = processResponse.data.id

      // ETAPA 2: CRIAR WORKFLOW
      const workflowResponse = await api.post('/workflows/', {
        workflow_type: selectedType.id,
        process_id: processId,
        client_id: 1, // TODO: Substituir por cliente real
        initial_data: {
          alteration_types: selectedAlterations.length > 0 ? selectedAlterations : undefined
        }
      })

      // VALIDAÇÃO 2: Workflow válido?
      if (!workflowResponse?.data?.id) {
        throw new Error('Workflow não foi criado')
      }

      if (!workflowResponse?.data?.stages || workflowResponse.data.stages.length === 0) {
        throw new Error('Workflow sem estágios definidos')
      }

      // ETAPA 3: NAVEGAÇÃO
      toast({
        title: 'Sucesso!',
        description: 'Processo automatizado criado com sucesso',
      })

      router.push(`/tenant/automation?workflow=${workflowResponse.data.id}`)

    } catch (err: any) {
      console.error('Erro ao criar processo:', err)
      toast({
        title: 'Erro',
        description: err.response?.data?.detail || err.message || 'Erro ao iniciar processo',
        variant: 'destructive'
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Agente de Contratos</h1>
        <p className="text-muted-foreground mt-1">
          Selecione o tipo de ato contratual que deseja elaborar
        </p>
      </div>

      {/* CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {contractTypes.map(type => {
          const Icon = type.icon
          return (
            <Card
              key={type.id}
              className="cursor-pointer hover:shadow-lg transition-shadow"
              onClick={() => handleCardClick(type)}
            >
              <CardHeader>
                <div className="flex items-center gap-3 mb-2">
                  <div className="p-2 bg-primary/10 rounded-lg">
                    <Icon className="h-5 w-5 text-primary" />
                  </div>
                  <CardTitle className="text-lg">{type.title}</CardTitle>
                </div>
                <CardDescription>{type.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" variant="outline">
                  Selecionar
                </Button>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* UM ÚNICO MODAL FORA DO MAP */}
      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              {selectedType?.icon && <selectedType.icon className="h-5 w-5" />}
              {selectedType?.title}
            </DialogTitle>
            <DialogDescription>
              {selectedType?.options.length === 0
                ? 'Confirme para iniciar o processo automatizado'
                : 'Escolha uma ou mais alterações que deseja realizar no contrato social'}
            </DialogDescription>
          </DialogHeader>

          {/* SE TEM OPÇÕES: CHECKBOXES */}
          {selectedType && selectedType.options.length > 0 && (
            <div className="space-y-4 py-4">
              {selectedType.options.map(opt => (
                <div key={opt.id} className="flex items-start space-x-3 p-3 border rounded-lg hover:bg-accent">
                  <Checkbox
                    id={opt.id}
                    checked={selectedAlterations.includes(opt.id)}
                    onCheckedChange={(checked) => handleCheckboxChange(opt.id, checked as boolean)}
                  />
                  <div className="flex-1">
                    <Label
                      htmlFor={opt.id}
                      className="font-semibold cursor-pointer"
                    >
                      {opt.label}
                    </Label>
                    <p className="text-sm text-muted-foreground mt-1">
                      {opt.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* SE NÃO TEM OPÇÕES: APENAS TEXTO */}
          {selectedType && selectedType.options.length === 0 && (
            <div className="py-4">
              <p className="text-sm text-muted-foreground">
                O sistema criará automaticamente um processo de {selectedType.title.toLowerCase()}
                com todas as etapas necessárias.
              </p>
            </div>
          )}

          <div className="flex gap-2 justify-end">
            <Button
              variant="outline"
              onClick={() => setIsModalOpen(false)}
              disabled={loading}
            >
              Cancelar
            </Button>
            <Button
              onClick={handleConfirm}
              disabled={
                loading ||
                (selectedType?.options.length! > 0 && selectedAlterations.length === 0)
              }
            >
              {loading ? 'Criando...' : `Confirmar${selectedAlterations.length > 0 ? ` (${selectedAlterations.length})` : ''}`}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}
