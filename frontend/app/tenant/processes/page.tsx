'use client'

import { useEffect, useState } from 'react'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import api from '@/lib/api'
import { FileText, Calendar, User, AlertCircle } from 'lucide-react'
import { useToast } from '@/components/ui/use-toast'
import { ProcessFormDialog } from '@/components/process-form-dialog'
import { ProcessEditDialog } from '@/components/process-edit-dialog'

interface Process {
  id: number
  client_id: number
  client_name?: string
  client_document?: string
  process_type: string
  title: string
  description?: string
  status: string
  priority: string
  estimated_days: number
  assigned_to?: number
  alteration_types?: string[]
  created_at: string
  updated_at: string
  started_at?: string
  completed_at?: string
}

export default function ProcessesPage() {
  const [processes, setProcesses] = useState<Process[]>([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState<any>(null)
  const { toast } = useToast()

  useEffect(() => {
    loadProcesses()
    loadStats()
  }, [])

  const loadProcesses = async () => {
    try {
      setLoading(true)
      const response = await api.get('/processes/')
      setProcesses(response.data.processes)
    } catch (err: any) {
      console.error('Erro ao carregar processos:', err)
      toast({
        title: 'Erro',
        description: 'Erro ao carregar processos',
        variant: 'destructive',
      })
    } finally {
      setLoading(false)
    }
  }

  const loadStats = async () => {
    try {
      const response = await api.get('/processes/stats')
      setStats(response.data)
    } catch (err) {
      console.error('Erro ao carregar estatísticas:', err)
    }
  }

  const getStatusColor = (status: string) => {
    const colors: any = {
      criado: 'bg-blue-100 text-blue-800',
      aguardando_docs: 'bg-yellow-100 text-yellow-800',
      em_andamento: 'bg-purple-100 text-purple-800',
      protocolado: 'bg-indigo-100 text-indigo-800',
      concluido: 'bg-green-100 text-green-800',
      cancelado: 'bg-red-100 text-red-800',
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  const getStatusText = (status: string) => {
    const labels: any = {
      criado: 'Criado',
      aguardando_docs: 'Aguardando Docs',
      em_andamento: 'Em Andamento',
      protocolado: 'Protocolado',
      concluido: 'Concluído',
      cancelado: 'Cancelado',
    }
    return labels[status] || status
  }

  const getTypeText = (type: string) => {
    const types: any = {
      abertura: 'Abertura de Empresa',
      alteracao: 'Alteração Contratual',
      regularizacao: 'Regularização',
      encerramento: 'Encerramento',
    }
    return types[type] || type
  }

  const getPriorityColor = (priority: string) => {
    const colors: any = {
      baixa: 'text-gray-600',
      normal: 'text-blue-600',
      alta: 'text-red-600',
    }
    return colors[priority] || 'text-gray-600'
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR')
  }

  const getAlterationName = (id: string) => {
    const names: Record<string, string> = {
      'endereco': 'Endereço',
      'socios': 'Sócios',
      'capital': 'Capital',
      'atividade': 'Atividade'
    }
    return names[id] || id
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-muted-foreground">Carregando processos...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Processos</h1>
          <p className="text-muted-foreground">
            Gerenciar processos de legalização
          </p>
        </div>
        <ProcessFormDialog onSuccess={loadProcesses} />
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total</CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.total || 0}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Aguardando</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.aguardando || 0}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Em Andamento</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.em_andamento || 0}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Concluído</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.concluido || 0}</div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Lista de Processos */}
      {processes.length === 0 ? (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-12">
              <FileText className="h-12 w-12 mx-auto mb-4 text-muted-foreground opacity-50" />
              <h3 className="text-lg font-medium mb-2">
                Nenhum processo cadastrado
              </h3>
              <p className="text-muted-foreground mb-4">
                Comece criando seu primeiro processo
              </p>
              <ProcessFormDialog onSuccess={loadProcesses} />
            </div>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>Lista de Processos</CardTitle>
            <CardDescription>
              {processes.length}{' '}
              {processes.length === 1
                ? 'processo cadastrado'
                : 'processos cadastrados'}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {processes.map((process) => (
                <div
                  key={process.id}
                  className="flex items-start justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                >
                  <div className="flex items-start gap-4 flex-1">
                    <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <FileText className="h-5 w-5 text-primary" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <p className="font-medium truncate">{process.title}</p>
                        <Badge variant="outline" className={getStatusColor(process.status)}>
                          {getStatusText(process.status)}
                        </Badge>
                      </div>
                      <div className="flex flex-wrap gap-3 text-sm text-muted-foreground">
                        <span className="flex items-center gap-1">
                          <User className="h-3 w-3" />
                          {process.client_name || 'Cliente não informado'}
                        </span>
                        <span>•</span>
                        <span>{getTypeText(process.process_type)}</span>
                        <span>•</span>
                        <span className={getPriorityColor(process.priority)}>
                          Prioridade: {process.priority}
                        </span>
                      </div>
                      {process.description && (
                        <p className="text-sm text-muted-foreground mt-2 line-clamp-2">
                          {process.description}
                        </p>
                      )}
                      {process.process_type === 'alteracao' && process.alteration_types && process.alteration_types.length > 0 && (
                        <div className="flex flex-wrap gap-2 mt-2">
                          {process.alteration_types.map(alt => (
                            <Badge key={alt} variant="outline" className="text-xs">
                              {getAlterationName(alt)}
                            </Badge>
                          ))}
                        </div>
                      )}
                      <div className="flex items-center gap-2 mt-2 text-xs text-muted-foreground">
                        <Calendar className="h-3 w-3" />
                        Criado em {formatDate(process.created_at)}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 ml-4">
                    <ProcessEditDialog
                      process={process}
                      onSuccess={loadProcesses}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
