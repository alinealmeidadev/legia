'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Checkbox } from '@/components/ui/checkbox'
import { Label } from '@/components/ui/label'
import { MapPin, Users, DollarSign, Briefcase } from 'lucide-react'

interface AlterationModalProps {
  open: boolean
  onClose: () => void
  onConfirm: (selectedTypes: string[]) => void
}

export function AlterationModal({ open, onClose, onConfirm }: AlterationModalProps) {
  const [selectedAlterations, setSelectedAlterations] = useState<string[]>([])

  const alterationTypes = [
    {
      id: 'endereco',
      nome: 'Alteração de Endereço',
      descricao: 'Mudança do endereço da sede da empresa',
      icon: MapPin,
      color: 'text-blue-500'
    },
    {
      id: 'socios',
      nome: 'Alteração de Sócios',
      descricao: 'Incluir, excluir ou alterar sócios',
      icon: Users,
      color: 'text-green-500'
    },
    {
      id: 'capital',
      nome: 'Alteração de Capital Social',
      descricao: 'Aumentar ou reduzir o capital social',
      icon: DollarSign,
      color: 'text-yellow-500'
    },
    {
      id: 'atividade',
      nome: 'Alteração de Atividade',
      descricao: 'Incluir ou excluir CNAEs',
      icon: Briefcase,
      color: 'text-purple-500'
    }
  ]

  const handleToggle = (alterationId: string) => {
    setSelectedAlterations(prev => {
      if (prev.includes(alterationId)) {
        return prev.filter(id => id !== alterationId)
      } else {
        return [...prev, alterationId]
      }
    })
  }

  const handleConfirm = () => {
    if (selectedAlterations.length > 0) {
      onConfirm(selectedAlterations)
      setSelectedAlterations([])
    }
  }

  const handleCancel = () => {
    setSelectedAlterations([])
    onClose()
  }

  return (
    <Dialog open={open} onOpenChange={handleCancel}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Selecione as Alterações</DialogTitle>
          <DialogDescription>
            Escolha uma ou mais alterações que deseja realizar no contrato social
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4">
          {alterationTypes.map((type) => {
            const Icon = type.icon
            const isSelected = selectedAlterations.includes(type.id)

            return (
              <div
                key={type.id}
                className={`flex items-start gap-4 p-4 border rounded-lg cursor-pointer transition-all ${
                  isSelected ? 'border-primary bg-primary/5' : 'hover:bg-accent/50'
                }`}
                onClick={() => handleToggle(type.id)}
              >
                <Checkbox
                  id={type.id}
                  checked={isSelected}
                  onCheckedChange={() => handleToggle(type.id)}
                />
                <div className="flex items-start gap-3 flex-1">
                  <div className={`p-2 rounded-lg ${type.color}`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  <div className="flex-1">
                    <Label
                      htmlFor={type.id}
                      className="text-base font-semibold cursor-pointer"
                    >
                      {type.nome}
                    </Label>
                    <p className="text-sm text-muted-foreground mt-1">
                      {type.descricao}
                    </p>
                  </div>
                </div>
              </div>
            )
          })}
        </div>

        {selectedAlterations.length === 0 && (
          <p className="text-sm text-muted-foreground text-center pb-2">
            Selecione pelo menos uma alteração para continuar
          </p>
        )}

        <DialogFooter>
          <Button
            type="button"
            variant="outline"
            onClick={handleCancel}
          >
            Cancelar
          </Button>
          <Button
            type="button"
            onClick={handleConfirm}
            disabled={selectedAlterations.length === 0}
          >
            Confirmar ({selectedAlterations.length})
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
