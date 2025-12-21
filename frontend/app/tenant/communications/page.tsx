'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Building, Search, Clock, CheckCircle, AlertCircle, FileText, ArrowRight } from 'lucide-react'

interface Protocol {
  id: number
  process_id: number
  client_name: string
  client_number: number
  organ: string
  protocol_number: string
  process_type: string
  status: string
  submitted_at: string
  estimated_conclusion: string
  last_update: string
}

export default function CommunicationsPage() {
  const [protocols, setProtocols] = useState<Protocol[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    loadProtocols()
  }, [])

  const loadProtocols = async () => {
    try {
      setLoading(true)
      // Dados mockados - API será implementada
      const mockData: Protocol[] = [
        {
          id: 1,
          process_id: 42,
          client_name: "ABC Contabilidade Ltda",
          client_number: 1001,
          organ: "Junta Comercial - JUCESP",
          protocol_number: "2025/123456",
          process_type: "Alteração Contratual",
          status: "em_analise",
          submitted_at: "2025-12-20T10:00:00",
          estimated_conclusion: "2025-12-28",
          last_update: "2025-12-21T14:30:00"
        }
      ]
      setProtocols(mockData)
    } catch (error) {
      console.error('Erro ao carregar protocolos:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusConfig = (status: string) => {
    const configs: Record<string, { label: string; color: string; icon: any }> = {
      em_analise: {
        label: 'Em Análise',
        color: 'bg-blue-100 text-blue-800 border-blue-200',
        icon: Clock
      },
      deferido: {
        label: 'Deferido',
        color: 'bg-green-100 text-green-800 border-green-200',
        icon: CheckCircle
      },
      pendente: {
        label: 'Pendente',
        color: 'bg-yellow-100 text-yellow-800 border-yellow-200',
        icon: AlertCircle
      },
      indeferido: {
        label: 'Indeferido',
        color: 'bg-red-100 text-red-800 border-red-200',
        icon: AlertCircle
      }
    }
    return configs[status] || configs.em_analise
  }

  const filteredProtocols = protocols.filter(p =>
    p.client_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.protocol_number.includes(searchTerm) ||
    p.client_number.toString().includes(searchTerm)
  )

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold">Acompanhamento de Protocolos</h1>
          <p className="text-muted-foreground mt-1">
            Monitore protocolos em órgãos públicos (Junta Comercial, Receita Federal, Prefeitura, etc.)
          </p>
        </div>
      </div>

      {/* Filtros */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Buscar por cliente, nº cliente ou protocolo..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <Button variant="outline">
              Filtrar por Órgão
            </Button>
            <Button variant="outline">
              Filtrar por Status
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Lista de Protocolos */}
      {loading ? (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-12">
              <p className="text-muted-foreground">Carregando protocolos...</p>
            </div>
          </CardContent>
        </Card>
      ) : filteredProtocols.length === 0 ? (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-12">
              <FileText className="h-12 w-12 mx-auto mb-4 text-muted-foreground opacity-50" />
              <h3 className="text-lg font-medium mb-2">Nenhum protocolo encontrado</h3>
              <p className="text-muted-foreground">
                {searchTerm
                  ? 'Tente ajustar sua busca'
                  : 'Protocolos aparecerão aqui quando processos forem enviados aos órgãos'
                }
              </p>
            </div>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4">
          {filteredProtocols.map((protocol) => {
            const statusConfig = getStatusConfig(protocol.status)
            const StatusIcon = statusConfig.icon

            return (
              <Card key={protocol.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <CardTitle className="text-lg">
                          Cliente #{protocol.client_number} - {protocol.client_name}
                        </CardTitle>
                        <Badge variant="outline" className={statusConfig.color}>
                          <StatusIcon className="h-3 w-3 mr-1" />
                          {statusConfig.label}
                        </Badge>
                      </div>
                      <CardDescription>
                        {protocol.process_type} • Processo #{protocol.process_id}
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div>
                      <p className="text-sm font-medium mb-1 flex items-center gap-1">
                        <Building className="h-3 w-3" />
                        Órgão
                      </p>
                      <p className="text-sm text-muted-foreground">{protocol.organ}</p>
                    </div>

                    <div>
                      <p className="text-sm font-medium mb-1">Nº Protocolo</p>
                      <p className="text-sm font-mono text-muted-foreground">{protocol.protocol_number}</p>
                    </div>

                    <div>
                      <p className="text-sm font-medium mb-1 flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        Previsão
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {new Date(protocol.estimated_conclusion).toLocaleDateString('pt-BR')}
                      </p>
                    </div>

                    <div>
                      <p className="text-sm font-medium mb-1">Última Atualização</p>
                      <p className="text-sm text-muted-foreground">
                        {new Date(protocol.last_update).toLocaleString('pt-BR', {
                          day: '2-digit',
                          month: '2-digit',
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </p>
                    </div>
                  </div>

                  <div className="flex gap-2 mt-4 pt-4 border-t">
                    <Button size="sm" variant="outline">
                      Ver Detalhes
                    </Button>
                    <Button size="sm" variant="outline">
                      Atualizar Status
                    </Button>
                    <Button size="sm" variant="outline">
                      <FileText className="h-4 w-4 mr-1" />
                      Documentos
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>
      )}

      {/* Informações */}
      <Card className="border-primary/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Building className="h-5 w-5" />
            Como funciona?
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <div className="flex items-start gap-2">
            <ArrowRight className="h-4 w-4 text-primary mt-0.5" />
            <span>Quando um processo é enviado para um órgão público, ele aparece aqui automaticamente</span>
          </div>
          <div className="flex items-start gap-2">
            <ArrowRight className="h-4 w-4 text-primary mt-0.5" />
            <span>O Agente Monitor verifica periodicamente o status nos sites dos órgãos</span>
          </div>
          <div className="flex items-start gap-2">
            <ArrowRight className="h-4 w-4 text-primary mt-0.5" />
            <span>Você recebe notificações quando houver mudanças de status</span>
          </div>
          <div className="flex items-start gap-2">
            <ArrowRight className="h-4 w-4 text-primary mt-0.5" />
            <span>Acompanhe: Junta Comercial, Receita Federal, Prefeitura, SEFAZ e outros</span>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
