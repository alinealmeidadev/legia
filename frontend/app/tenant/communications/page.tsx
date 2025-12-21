'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Mail, Send, Calendar, User, Building } from 'lucide-react'

interface Communication {
  id: number
  type: string
  recipient_organ: string
  subject: string
  body: string
  status: string
  created_at: string
  sent_at?: string
}

export default function CommunicationsPage() {
  const [communications, setCommunications] = useState<Communication[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadCommunications()
  }, [])

  const loadCommunications = async () => {
    try {
      setLoading(true)
      // Por enquanto, dados mockados - a API será implementada depois
      setCommunications([])
    } catch (error) {
      console.error('Erro ao carregar comunicações:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      draft: 'bg-gray-100 text-gray-800',
      sent: 'bg-blue-100 text-blue-800',
      delivered: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  const getStatusText = (status: string) => {
    const labels: Record<string, string> = {
      draft: 'Rascunho',
      sent: 'Enviado',
      delivered: 'Entregue',
      failed: 'Falhou',
    }
    return labels[status] || status
  }

  const getTypeText = (type: string) => {
    const types: Record<string, string> = {
      email: 'Email',
      oficio: 'Ofício',
      requerimento: 'Requerimento',
      recurso: 'Recurso',
    }
    return types[type] || type
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-muted-foreground">Carregando comunicações...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Comunicações</h1>
          <p className="text-muted-foreground mt-1">
            Gerenciar comunicações com órgãos
          </p>
        </div>
        <Button>
          <Send className="mr-2 h-4 w-4" />
          Nova Comunicação
        </Button>
      </div>

      {communications.length === 0 ? (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-12">
              <Mail className="h-12 w-12 mx-auto mb-4 text-muted-foreground opacity-50" />
              <h3 className="text-lg font-medium mb-2">Nenhuma comunicação</h3>
              <p className="text-muted-foreground mb-4">
                Comece criando sua primeira comunicação
              </p>
              <Button>
                <Send className="mr-2 h-4 w-4" />
                Nova Comunicação
              </Button>
            </div>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>Histórico de Comunicações</CardTitle>
            <CardDescription>
              {communications.length}{' '}
              {communications.length === 1 ? 'comunicação registrada' : 'comunicações registradas'}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {communications.map((comm) => (
                <div
                  key={comm.id}
                  className="flex items-start justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                >
                  <div className="flex items-start gap-4 flex-1">
                    <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <Mail className="h-5 w-5 text-primary" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <p className="font-medium truncate">{comm.subject}</p>
                        <Badge variant="outline" className={getStatusColor(comm.status)}>
                          {getStatusText(comm.status)}
                        </Badge>
                      </div>
                      <div className="flex flex-wrap gap-3 text-sm text-muted-foreground mb-2">
                        <span>{getTypeText(comm.type)}</span>
                        <span>•</span>
                        <span className="flex items-center gap-1">
                          <Building className="h-3 w-3" />
                          {comm.recipient_organ}
                        </span>
                      </div>
                      <p className="text-sm text-muted-foreground line-clamp-2">
                        {comm.body}
                      </p>
                      <div className="flex items-center gap-2 mt-2 text-xs text-muted-foreground">
                        <Calendar className="h-3 w-3" />
                        Criado em {formatDate(comm.created_at)}
                        {comm.sent_at && ` • Enviado em ${formatDate(comm.sent_at)}`}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 ml-4">
                    <Button variant="outline" size="sm">
                      Ver Detalhes
                    </Button>
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
