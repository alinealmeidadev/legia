'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import AlterationModal from '@/components/alteration-modal'
import api from '@/lib/api'

type Act = {
  id: number
  name: string
}

export default function ContractsPage() {
  const router = useRouter()

  const [acts, setActs] = useState<Act[]>([])
  const [selectedAct, setSelectedAct] = useState<number | null>(null)
  const [selectedAlterations, setSelectedAlterations] = useState<string[]>([])
  const [showAlterationModal, setShowAlterationModal] = useState(false)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    api.get('/contracts/acts').then(res => setActs(res.data))
  }, [])

  const handleSelectAct = (id: number) => {
    setSelectedAct(id)
    setShowAlterationModal(true)
  }

  const handleAlterationConfirm = (alterations: string[]) => {
    setSelectedAlterations(alterations)
    setShowAlterationModal(false)
  }

  /**
   * 🔴 FUNÇÃO CRÍTICA — FLUXO CORRETO
   */
  const handleCreateProcess = async () => {
    if (selectedAlterations.length === 0) {
      alert('Selecione pelo menos uma alteração')
      return
    }

    try {
      setLoading(true)

      /** ETAPA 1 — CRIAR PROCESSO */
      const processResponse = await api.post('/processes/', {
        process_type: 'alteracao',
        title: 'Alteração Contratual',
        description: `Alterações: ${selectedAlterations.join(', ')}`,
        client_id: selectedAct,
        alteration_types: selectedAlterations,
        priority: 'normal',
        status: 'aguardando'
      })

      if (!processResponse?.data?.id) {
        throw new Error('Processo não foi criado')
      }

      const processId = processResponse.data.id

      /** ETAPA 2 — CRIAR WORKFLOW */
      const workflowResponse = await api.post('/workflows/', {
        workflow_type: 'alteracao',
        process_id: processId,
        client_id: selectedAct,
        initial_data: {
          alteration_types: selectedAlterations
        }
      })

      if (!workflowResponse?.data?.id) {
        throw new Error('Workflow não foi criado')
      }

      /** ETAPA 3 — NAVEGAÇÃO */
      router.push(`/tenant/automation?workflow=${workflowResponse.data.id}`)

    } catch (err: any) {
      console.error(err)
      alert(
        err.response?.data?.detail ||
        err.message ||
        'Erro ao iniciar processo'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6 space-y-6">

      <AlterationModal
        open={showAlterationModal}
        onClose={() => setShowAlterationModal(false)}
        onConfirm={handleAlterationConfirm}
      />

      {!selectedAlterations.length ? (
        <div className="grid grid-cols-3 gap-4">
          {acts.map(act => (
            <Card
              key={act.id}
              className="p-4 cursor-pointer hover:border-primary"
              onClick={() => handleSelectAct(act.id)}
            >
              {act.name}
            </Card>
          ))}
        </div>
      ) : (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">
            Alterações selecionadas
          </h2>

          <ul className="list-disc pl-5">
            {selectedAlterations.map(item => (
              <li key={item}>{item}</li>
            ))}
          </ul>

          <Button
            size="lg"
            className="w-full"
            onClick={handleCreateProcess}
            disabled={loading}
          >
            {loading ? 'Criando...' : 'Iniciar Novo Processo'}
          </Button>
        </div>
      )}
    </div>
  )
}
