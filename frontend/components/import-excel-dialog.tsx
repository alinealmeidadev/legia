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
  DialogTrigger,
} from '@/components/ui/dialog'
import { useToast } from '@/components/ui/use-toast'
import api from '@/lib/api'
import { FileSpreadsheet, Upload, Download, Loader2, AlertCircle, CheckCircle } from 'lucide-react'
import { Badge } from '@/components/ui/badge'

interface ImportExcelDialogProps {
  onSuccess?: () => void
}

export function ImportExcelDialog({ onSuccess }: ImportExcelDialogProps) {
  const [open, setOpen] = useState(false)
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [importing, setImporting] = useState(false)
  const [preview, setPreview] = useState<any>(null)
  const { toast } = useToast()

  const downloadTemplate = async () => {
    try {
      const response = await api.get('/clients/utils/template-excel', {
        responseType: 'blob'
      })

      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'template_importacao_clientes.xlsx')
      document.body.appendChild(link)
      link.click()
      link.remove()

      toast({
        title: 'Sucesso!',
        description: 'Template baixado com sucesso',
      })
    } catch (error: any) {
      toast({
        variant: 'destructive',
        title: 'Erro',
        description: 'Erro ao baixar template',
      })
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setPreview(null)
    }
  }

  const processFile = async () => {
    if (!file) return

    setLoading(true)

    try {
      const formData = new FormData()
      formData.append('arquivo', file)

      const response = await api.post('/clients/utils/importar-excel', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      setPreview(response.data)

      toast({
        title: 'Arquivo processado!',
        description: `${response.data.total_validos} cliente(s) válido(s) encontrado(s)`,
      })
    } catch (error: any) {
      toast({
        variant: 'destructive',
        title: 'Erro ao processar arquivo',
        description: error.response?.data?.detail || 'Erro desconhecido',
      })
    } finally {
      setLoading(false)
    }
  }

  const confirmImport = async () => {
    if (!preview || !preview.clientes) return

    setImporting(true)

    try {
      const response = await api.post('/clients/utils/confirmar-importacao',
        preview.clientes
      )

      toast({
        title: 'Sucesso!',
        description: `${response.data.inseridos} cliente(s) importado(s)`,
      })

      setOpen(false)
      setFile(null)
      setPreview(null)

      if (onSuccess) {
        onSuccess()
      }
    } catch (error: any) {
      toast({
        variant: 'destructive',
        title: 'Erro ao importar',
        description: error.response?.data?.detail || 'Erro desconhecido',
      })
    } finally {
      setImporting(false)
    }
  }

  const reset = () => {
    setFile(null)
    setPreview(null)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline">
          <FileSpreadsheet className="mr-2 h-4 w-4" />
          Importar Excel
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Importação em Lote de Clientes</DialogTitle>
          <DialogDescription>
            Faça upload de um arquivo Excel para importar múltiplos clientes de uma vez
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4">
          {/* Passo 1: Baixar Template */}
          <div className="border rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <span className="font-semibold">1. Baixar Template</span>
            </div>
            <p className="text-sm text-muted-foreground mb-3">
              Baixe o template Excel e preencha com os dados dos clientes
            </p>
            <Button variant="outline" onClick={downloadTemplate}>
              <Download className="mr-2 h-4 w-4" />
              Baixar Template Excel
            </Button>
          </div>

          {/* Passo 2: Upload */}
          <div className="border rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <span className="font-semibold">2. Fazer Upload do Arquivo</span>
            </div>
            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={handleFileChange}
              className="mb-3"
            />
            {file && (
              <div className="flex items-center gap-2 text-sm mb-3">
                <FileSpreadsheet className="h-4 w-4" />
                <span>{file.name}</span>
              </div>
            )}
            <Button
              onClick={processFile}
              disabled={!file || loading}
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Processando...
                </>
              ) : (
                <>
                  <Upload className="mr-2 h-4 w-4" />
                  Processar Arquivo
                </>
              )}
            </Button>
          </div>

          {/* Passo 3: Preview e Confirmação */}
          {preview && (
            <div className="border rounded-lg p-4">
              <div className="flex items-center gap-2 mb-4">
                <span className="font-semibold">3. Revisar e Confirmar</span>
              </div>

              {/* Estatísticas */}
              <div className="grid grid-cols-3 gap-4 mb-4">
                <div className="text-center p-3 border rounded">
                  <div className="text-2xl font-bold">{preview.total_linhas}</div>
                  <div className="text-sm text-muted-foreground">Total Linhas</div>
                </div>
                <div className="text-center p-3 border rounded bg-green-50">
                  <div className="text-2xl font-bold text-green-600">{preview.total_validos}</div>
                  <div className="text-sm text-muted-foreground">Válidos</div>
                </div>
                <div className="text-center p-3 border rounded bg-red-50">
                  <div className="text-2xl font-bold text-red-600">{preview.total_erros}</div>
                  <div className="text-sm text-muted-foreground">Erros</div>
                </div>
              </div>

              {/* Erros */}
              {preview.erros && preview.erros.length > 0 && (
                <div className="mb-4">
                  <div className="flex items-center gap-2 mb-2 text-red-600">
                    <AlertCircle className="h-4 w-4" />
                    <span className="font-semibold">Erros Encontrados</span>
                  </div>
                  <div className="max-h-40 overflow-y-auto space-y-1">
                    {preview.erros.slice(0, 10).map((erro: string, index: number) => (
                      <div key={index} className="text-sm text-red-600 bg-red-50 p-2 rounded">
                        {erro}
                      </div>
                    ))}
                    {preview.erros.length > 10 && (
                      <div className="text-sm text-muted-foreground">
                        ... e mais {preview.erros.length - 10} erro(s)
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Preview dos clientes válidos */}
              {preview.clientes && preview.clientes.length > 0 && (
                <div className="mb-4">
                  <div className="flex items-center gap-2 mb-2 text-green-600">
                    <CheckCircle className="h-4 w-4" />
                    <span className="font-semibold">Clientes Válidos (Preview)</span>
                  </div>
                  <div className="max-h-60 overflow-y-auto space-y-2">
                    {preview.clientes.slice(0, 5).map((item: any) => (
                      <div key={item.linha} className="border rounded p-3 text-sm">
                        <div className="flex items-center gap-2 mb-1">
                          <Badge variant="outline">{item.dados.type === 'pf' ? 'PF' : 'PJ'}</Badge>
                          <span className="font-semibold">{item.dados.name}</span>
                        </div>
                        <div className="text-muted-foreground">
                          {item.dados.document} - {item.dados.email || 'Sem email'}
                        </div>
                      </div>
                    ))}
                    {preview.clientes.length > 5 && (
                      <div className="text-sm text-muted-foreground text-center">
                        ... e mais {preview.clientes.length - 5} cliente(s)
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Botão de Confirmação */}
              {preview.total_validos > 0 && (
                <Button
                  className="w-full"
                  onClick={confirmImport}
                  disabled={importing}
                >
                  {importing ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Importando...
                    </>
                  ) : (
                    <>
                      Confirmar Importação de {preview.total_validos} Cliente(s)
                    </>
                  )}
                </Button>
              )}
            </div>
          )}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => { setOpen(false); reset(); }}>
            Fechar
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
