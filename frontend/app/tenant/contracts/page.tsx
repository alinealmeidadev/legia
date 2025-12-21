'use client'

import { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { AlterationModal } from '@/components/alteration-modal'
import {
  FileText,
  MapPin,
  Users,
  DollarSign,
  Briefcase,
  Building,
  User,
  XCircle,
  Clock,
  CheckCircle
} from 'lucide-react'

interface Act {
  id: string
  nome: string
  descricao: string
  prazo: string
  documentos: number
}

interface ActDetails {
  nome: string
  descricao: string
  campos_necessarios: string[]
  documentos_necessarios: string[]
  prazo_medio: string
  orgaos: string[]
}

export default function ContractsPage() {
  const [acts, setActs] = useState<Act[]>([])
  const [selectedAct, setSelectedAct] = useState<string | null>(null)
  const [actDetails, setActDetails] = useState<ActDetails | null>(null)
  const [loading, setLoading] = useState(false)
  const [showAlterationModal, setShowAlterationModal] = useState(false)
  const [selectedAlterations, setSelectedAlterations] = useState<string[]>([])

  useEffect(() => {
    loadActs()
  }, [])

  const loadActs = async () => {
    try {
      setLoading(true)
      const response = await api.get('/contracts/acts')
      setActs(response.data)
    } catch (error) {
      console.error('Erro ao carregar atos:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSelectAct = async (actId: string) => {
    try {
      setSelectedAct(actId)

      // Se for alteração contratual, abrir modal de seleção múltipla
      if (actId.startsWith('alteracao')) {
        setShowAlterationModal(true)
        return
      }

      setLoading(true)
      const response = await api.get(`/contracts/acts/${actId}`)
      setActDetails(response.data)
    } catch (error) {
      console.error('Erro ao carregar detalhes do ato:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAlterationConfirm = async (alterations: string[]) => {
    setSelectedAlterations(alterations)
    setShowAlterationModal(false)

    // Carregar detalhes com as alterações selecionadas
    try {
      setLoading(true)
      const response = await api.post('/contracts/acts/multiple', {
        alteration_types: alterations
      })
      setActDetails(response.data)
    } catch (error) {
      console.error('Erro ao carregar detalhes das alterações:', error)
    } finally {
      setLoading(false)
    }
  }

  const getActIcon = (actId: string) => {
    const icons: Record<string, any> = {
      'alteracao_endereco': MapPin,
      'alteracao_socios': Users,
      'alteracao_capital': DollarSign,
      'alteracao_atividade': Briefcase,
      'alteracao_nome': Building,
      'alteracao_administracao': User,
      'distrato': XCircle
    }
    return icons[actId] || FileText
  }

  return (
    <>
      <AlterationModal
        open={showAlterationModal}
        onClose={() => {
          setShowAlterationModal(false)
          setSelectedAct(null)
        }}
        onConfirm={handleAlterationConfirm}
      />

      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold">Agente de Contratos</h1>
          <p className="text-muted-foreground mt-1">
            Selecione o tipo de ato contratual que deseja elaborar
          </p>
        </div>

      {!selectedAct ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {loading ? (
            <div className="col-span-full text-center py-12">
              <p className="text-muted-foreground">Carregando atos disponíveis...</p>
            </div>
          ) : (
            acts.map((act) => {
              const Icon = getActIcon(act.id)
              return (
                <Card
                  key={act.id}
                  className="cursor-pointer hover:shadow-lg transition-shadow"
                  onClick={() => handleSelectAct(act.id)}
                >
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-primary/10 rounded-lg">
                          <Icon className="h-5 w-5 text-primary" />
                        </div>
                        <div>
                          <CardTitle className="text-lg">{act.nome}</CardTitle>
                        </div>
                      </div>
                    </div>
                    <CardDescription className="mt-2">
                      {act.descricao}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center gap-1 text-muted-foreground">
                        <Clock className="h-4 w-4" />
                        <span>{act.prazo}</span>
                      </div>
                      <Badge variant="secondary">
                        {act.documentos} docs
                      </Badge>
                    </div>
                  </CardContent>
                </Card>
              )
            })
          )}
        </div>
      ) : (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold">{actDetails?.nome}</h2>
              <p className="text-muted-foreground">{actDetails?.descricao}</p>
            </div>
            <Button
              variant="outline"
              onClick={() => {
                setSelectedAct(null)
                setActDetails(null)
              }}
            >
              Voltar
            </Button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Informações do Ato */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <CardTitle>Informações do Ato</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Prazo */}
                <div>
                  <h3 className="font-semibold mb-2 flex items-center gap-2">
                    <Clock className="h-4 w-4" />
                    Prazo Estimado
                  </h3>
                  <p className="text-muted-foreground">{actDetails?.prazo_medio}</p>
                </div>

                {/* Órgãos */}
                <div>
                  <h3 className="font-semibold mb-2">Órgãos Envolvidos</h3>
                  <div className="flex flex-wrap gap-2">
                    {actDetails?.orgaos.map((orgao) => (
                      <Badge key={orgao} variant="secondary">
                        {orgao}
                      </Badge>
                    ))}
                  </div>
                </div>

                {/* Campos Necessários */}
                <div>
                  <h3 className="font-semibold mb-2">Dados Necessários</h3>
                  <ul className="space-y-2">
                    {actDetails?.campos_necessarios.map((campo) => (
                      <li key={campo} className="flex items-center gap-2 text-sm">
                        <CheckCircle className="h-4 w-4 text-green-600" />
                        <span className="capitalize">{campo.replace(/_/g, ' ')}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Documentos Necessários */}
                <div>
                  <h3 className="font-semibold mb-2">Documentos Necessários</h3>
                  <ul className="space-y-2">
                    {actDetails?.documentos_necessarios.map((doc) => (
                      <li key={doc} className="flex items-center gap-2 text-sm">
                        <FileText className="h-4 w-4 text-blue-600" />
                        <span className="capitalize">{doc.replace(/_/g, ' ')}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </CardContent>
            </Card>

            {/* Ações */}
            <Card>
              <CardHeader>
                <CardTitle>Ações</CardTitle>
                <CardDescription>
                  Escolha como prosseguir com este ato
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button className="w-full" size="lg">
                  Iniciar Novo Processo
                </Button>

                <Button className="w-full" variant="outline">
                  Fazer Upload de Documentos
                </Button>

                <Button className="w-full" variant="outline">
                  Buscar Empresa Existente
                </Button>

                <div className="pt-4 border-t">
                  <Button className="w-full" variant="secondary">
                    Ver Checklist Completo
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Alterações Selecionadas */}
          {selectedAlterations.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Alterações Selecionadas</CardTitle>
                <CardDescription>
                  Você selecionou {selectedAlterations.length} tipo(s) de alteração
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {selectedAlterations.map((alt) => (
                    <Badge key={alt} variant="secondary">
                      {alt === 'endereco' && 'Endereço'}
                      {alt === 'socios' && 'Sócios'}
                      {alt === 'capital' && 'Capital Social'}
                      {alt === 'atividade' && 'Atividade'}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Preview/Formulário */}
          <Card>
            <CardHeader>
              <CardTitle>Formulário de Dados</CardTitle>
              <CardDescription>
                Preencha as informações necessárias para gerar o documento
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12 text-muted-foreground">
                <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>Funcionalidade em desenvolvimento</p>
                <p className="text-sm mt-2">
                  Em breve você poderá preencher formulários inteligentes e gerar documentos automaticamente
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
      </div>
    </>
  )
}
