'use client'

import { useState } from 'react'
import { api } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import {
  Rocket,
  MapPin,
  Users,
  DollarSign,
  Briefcase,
  Building,
  CheckCircle,
  Clock,
  ArrowRight
} from 'lucide-react'

export default function AutomationPage() {
  const [selectedType, setSelectedType] = useState<string | null>(null)
  const [workflow, setWorkflow] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Tipos de processo disponíveis
  const processTypes = [
    {
      id: 'alteracao_endereco',
      nome: 'Alteração de Endereço',
      descricao: 'Mudar o endereço da sede da empresa',
      icon: MapPin,
      color: 'bg-blue-500'
    },
    {
      id: 'alteracao_socios',
      nome: 'Alteração de Sócios',
      descricao: 'Incluir, excluir ou alterar sócios',
      icon: Users,
      color: 'bg-green-500'
    },
    {
      id: 'alteracao_capital',
      nome: 'Alteração de Capital',
      descricao: 'Aumentar ou reduzir capital social',
      icon: DollarSign,
      color: 'bg-yellow-500'
    },
    {
      id: 'alteracao_atividade',
      nome: 'Alteração de Atividade',
      descricao: 'Incluir ou excluir CNAEs',
      icon: Briefcase,
      color: 'bg-purple-500'
    },
    {
      id: 'abertura_empresa',
      nome: 'Abertura de Empresa',
      descricao: 'Constituir nova empresa',
      icon: Building,
      color: 'bg-red-500'
    }
  ]

  const startAutomation = async (processType: string) => {
    try {
      setLoading(true)
      setError('')

      // Criar workflow automatizado
      const response = await api.post('/workflows/', {
        workflow_type: processType,
        client_id: 1, // Por enquanto usando ID fixo
        initial_data: {}
      })

      setWorkflow(response.data)
      setSelectedType(processType)
    } catch (err: any) {
      console.error('Erro ao criar workflow:', err)
      setError(err.response?.data?.detail || 'Erro ao iniciar automação')
    } finally {
      setLoading(false)
    }
  }

  const getStageIcon = (stage: string) => {
    const icons: Record<string, any> = {
      'commercial': DollarSign,
      'legalization': CheckCircle,
      'client_form': MapPin,
      'document_collection': Users,
      'contracts': Building,
      'protocol': Briefcase,
      'monitoring': Clock,
      'completed': CheckCircle
    }
    return icons[stage] || Clock
  }

  if (workflow) {
    const currentStage = workflow.stages.find((s: any) => s.stage === workflow.current_stage)

    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Processo Automatizado</h1>
            <p className="text-muted-foreground mt-1">
              Workflow ID: {workflow.id}
            </p>
          </div>
          <Button
            variant="outline"
            onClick={() => {
              setWorkflow(null)
              setSelectedType(null)
            }}
          >
            Voltar
          </Button>
        </div>

        {/* Progresso */}
        <Card>
          <CardHeader>
            <CardTitle>Progresso do Processo</CardTitle>
            <CardDescription>
              Estágio atual: {currentStage?.name}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {workflow.stages.map((stage: any, index: number) => {
                const Icon = getStageIcon(stage.stage)
                const isCurrent = stage.stage === workflow.current_stage
                const isCompleted = stage.completed

                return (
                  <div
                    key={stage.stage}
                    className={`flex items-start gap-4 p-4 rounded-lg border ${
                      isCurrent ? 'border-primary bg-primary/5' : ''
                    } ${isCompleted ? 'bg-green-50 border-green-200' : ''}`}
                  >
                    <div className={`p-2 rounded-lg ${
                      isCompleted ? 'bg-green-500 text-white' :
                      isCurrent ? 'bg-primary text-white' :
                      'bg-gray-200 text-gray-500'
                    }`}>
                      <Icon className="h-5 w-5" />
                    </div>

                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <h3 className="font-semibold">{stage.name}</h3>
                        {isCompleted && (
                          <Badge variant="default" className="bg-green-500">
                            Concluído
                          </Badge>
                        )}
                        {isCurrent && (
                          <Badge variant="default">
                            Em Andamento
                          </Badge>
                        )}
                      </div>
                      <p className="text-sm text-muted-foreground mt-1">
                        {stage.description}
                      </p>
                      {stage.agent && (
                        <p className="text-xs text-muted-foreground mt-2">
                          Agente: {stage.agent}
                        </p>
                      )}
                    </div>

                    {!isCompleted && index < workflow.stages.length - 1 && (
                      <ArrowRight className="h-5 w-5 text-muted-foreground mt-2" />
                    )}
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>

        {/* Histórico */}
        {workflow.history && workflow.history.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Histórico</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {workflow.history.map((event: any, index: number) => (
                  <div key={index} className="flex items-start gap-3 text-sm">
                    <span className="text-muted-foreground">
                      {new Date(event.timestamp).toLocaleString('pt-BR')}
                    </span>
                    <span>-</span>
                    <span>{event.description}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Formulários */}
        {workflow.forms && workflow.forms.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle>Formulário Gerado</CardTitle>
              <CardDescription>
                O sistema gerou automaticamente um formulário para coletar dados
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Badge variant="secondary" className="mb-4">
                {workflow.forms.length} formulário(s) disponível(is)
              </Badge>
              <p className="text-sm text-muted-foreground">
                Em produção, o cliente receberia este formulário por email/WhatsApp
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <Rocket className="h-8 w-8 text-primary" />
          Automação de Processos
        </h1>
        <p className="text-muted-foreground mt-2">
          Inicie um processo totalmente automatizado. Os agentes trabalharão juntos para completar tudo!
        </p>
      </div>

      {error && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="pt-6">
            <p className="text-red-600">{error}</p>
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {processTypes.map((type) => {
          const Icon = type.icon

          return (
            <Card
              key={type.id}
              className="cursor-pointer hover:shadow-lg transition-all hover:scale-105"
              onClick={() => !loading && startAutomation(type.id)}
            >
              <CardHeader>
                <div className={`w-12 h-12 rounded-lg ${type.color} flex items-center justify-center mb-3`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
                <CardTitle className="text-lg">{type.nome}</CardTitle>
                <CardDescription>{type.descricao}</CardDescription>
              </CardHeader>
              <CardContent>
                <Button
                  className="w-full"
                  disabled={loading}
                >
                  {loading ? 'Iniciando...' : 'Iniciar Automação'}
                </Button>
              </CardContent>
            </Card>
          )
        })}
      </div>

      <Card className="border-primary">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Rocket className="h-5 w-5" />
            Como Funciona?
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="flex items-start gap-2">
            <span className="font-bold text-primary">1.</span>
            <span>Você clica em um tipo de processo acima</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="font-bold text-primary">2.</span>
            <span>Sistema cria workflow automatizado com múltiplos agentes</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="font-bold text-primary">3.</span>
            <span>Agente Comercial gera orçamento</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="font-bold text-primary">4.</span>
            <span>Agente de Legalização analisa viabilidade</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="font-bold text-primary">5.</span>
            <span>Sistema gera formulário inteligente para o cliente</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="font-bold text-primary">6.</span>
            <span>Agente de Contratos gera documentos</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="font-bold text-primary">7.</span>
            <span>Agente de Protocolos envia para órgãos</span>
          </div>
          <div className="flex items-start gap-2">
            <span className="font-bold text-primary">8.</span>
            <span>Agente Monitor acompanha até conclusão</span>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
