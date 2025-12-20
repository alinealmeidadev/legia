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
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Plus, Search, Loader2 } from 'lucide-react'
import api from '@/lib/api'
import { useToast } from '@/components/ui/use-toast'

interface ClientFormDialogProps {
  onSuccess?: () => void
}

export function ClientFormDialog({ onSuccess }: ClientFormDialogProps) {
  const [open, setOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const [consultingCNPJ, setConsultingCNPJ] = useState(false)
  const [consultingCEP, setConsultingCEP] = useState(false)
  const [documentoValido, setDocumentoValido] = useState<boolean | null>(null)
  const { toast } = useToast()

  const [formData, setFormData] = useState({
    type: 'pf',
    name: '',
    document: '',
    email: '',
    phone: '',
    mobile: '',
    // Dados PJ
    company_name: '',
    trade_name: '',
    cnae_primary: '',
    state_registration: '',
    municipal_registration: '',
    // Endereço
    address_street: '',
    address_number: '',
    address_complement: '',
    address_neighborhood: '',
    address_city: '',
    address_state: '',
    address_zipcode: '',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const data = {
        type: formData.type,
        name: formData.name,
        document: formData.document,
        email: formData.email || undefined,
        phone: formData.phone || undefined,
        mobile: formData.mobile || undefined,
        // Dados PJ (apenas se for PJ)
        company_name: formData.type === 'pj' ? formData.company_name || undefined : undefined,
        trade_name: formData.type === 'pj' ? formData.trade_name || undefined : undefined,
        cnae_primary: formData.type === 'pj' ? formData.cnae_primary || undefined : undefined,
        state_registration: formData.type === 'pj' ? formData.state_registration || undefined : undefined,
        municipal_registration: formData.type === 'pj' ? formData.municipal_registration || undefined : undefined,
        // Endereço
        address_street: formData.address_street || undefined,
        address_number: formData.address_number || undefined,
        address_complement: formData.address_complement || undefined,
        address_neighborhood: formData.address_neighborhood || undefined,
        address_city: formData.address_city || undefined,
        address_state: formData.address_state || undefined,
        address_zipcode: formData.address_zipcode || undefined,
      }

      await api.post('/clients/', data)

      toast({
        title: 'Sucesso!',
        description: 'Cliente criado com sucesso.',
      })

      setOpen(false)
      setFormData({
        type: 'pf',
        name: '',
        document: '',
        email: '',
        phone: '',
        mobile: '',
        company_name: '',
        trade_name: '',
        cnae_primary: '',
        state_registration: '',
        municipal_registration: '',
        address_street: '',
        address_number: '',
        address_complement: '',
        address_neighborhood: '',
        address_city: '',
        address_state: '',
        address_zipcode: '',
      })

      if (onSuccess) {
        onSuccess()
      }
    } catch (error: any) {
      console.error('Erro ao criar cliente:', error)
      toast({
        variant: 'destructive',
        title: 'Erro',
        description: error.response?.data?.detail || 'Erro ao criar cliente.',
      })
    } finally {
      setLoading(false)
    }
  }

  const formatCPF = (value: string) => {
    const numbers = value.replace(/\D/g, '')
    if (numbers.length <= 11) {
      return numbers
        .replace(/^(\d{3})(\d)/, '$1.$2')
        .replace(/^(\d{3})\.(\d{3})(\d)/, '$1.$2.$3')
        .replace(/\.(\d{3})(\d)/, '.$1-$2')
    }
    return value
  }

  const formatCNPJ = (value: string) => {
    const numbers = value.replace(/\D/g, '')
    if (numbers.length <= 14) {
      return numbers
        .replace(/^(\d{2})(\d)/, '$1.$2')
        .replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
        .replace(/\.(\d{3})(\d)/, '.$1/$2')
        .replace(/(\d{4})(\d)/, '$1-$2')
    }
    return value
  }

  const formatCEP = (value: string) => {
    const numbers = value.replace(/\D/g, '')
    if (numbers.length <= 8) {
      return numbers.replace(/^(\d{5})(\d)/, '$1-$2')
    }
    return value
  }

  const handleDocumentChange = async (value: string) => {
    const formatted = formData.type === 'pf' ? formatCPF(value) : formatCNPJ(value)
    setFormData({ ...formData, document: formatted })

    // Validar documento quando estiver completo
    const docLimpo = formatted.replace(/\D/g, '')
    const tamanhoEsperado = formData.type === 'pf' ? 11 : 14

    if (docLimpo.length === tamanhoEsperado) {
      try {
        const response = await api.get(`/clients/utils/validar-documento/${docLimpo}`)
        setDocumentoValido(response.data.valido)

        if (!response.data.valido) {
          toast({
            variant: 'destructive',
            title: `${formData.type === 'pf' ? 'CPF' : 'CNPJ'} inválido`,
            description: 'Por favor, verifique o documento informado',
          })
        }
      } catch (error) {
        setDocumentoValido(null)
      }
    } else {
      setDocumentoValido(null)
    }
  }

  const consultarCNPJ = async () => {
    if (formData.type !== 'pj') return

    const cnpjLimpo = formData.document.replace(/\D/g, '')
    if (cnpjLimpo.length !== 14) {
      toast({
        variant: 'destructive',
        title: 'Erro',
        description: 'CNPJ deve conter 14 dígitos',
      })
      return
    }

    setConsultingCNPJ(true)

    try {
      const response = await api.get(`/clients/utils/consultar-cnpj/${cnpjLimpo}`)
      const dados = response.data.data

      // Preencher automaticamente os campos
      setFormData({
        ...formData,
        name: dados.razao_social || formData.name,
        company_name: dados.razao_social || formData.company_name,
        trade_name: dados.nome_fantasia || formData.trade_name,
        email: dados.email || formData.email,
        phone: dados.telefone || formData.phone,
        address_street: dados.logradouro || formData.address_street,
        address_number: dados.numero || formData.address_number,
        address_complement: dados.complemento || formData.address_complement,
        address_neighborhood: dados.bairro || formData.address_neighborhood,
        address_city: dados.municipio || formData.address_city,
        address_state: dados.uf || formData.address_state,
        address_zipcode: dados.cep ? formatCEP(dados.cep) : formData.address_zipcode,
      })

      toast({
        title: 'Sucesso!',
        description: 'Dados do CNPJ carregados automaticamente',
      })
    } catch (error: any) {
      toast({
        variant: 'destructive',
        title: 'Erro ao consultar CNPJ',
        description: error.response?.data?.detail || 'Não foi possível consultar o CNPJ',
      })
    } finally {
      setConsultingCNPJ(false)
    }
  }

  const consultarCEP = async () => {
    const cepLimpo = formData.address_zipcode.replace(/\D/g, '')
    if (cepLimpo.length !== 8) {
      toast({
        variant: 'destructive',
        title: 'Erro',
        description: 'CEP deve conter 8 dígitos',
      })
      return
    }

    setConsultingCEP(true)

    try {
      const response = await api.get(`/clients/utils/consultar-cep/${cepLimpo}`)
      const dados = response.data.data

      // Preencher automaticamente os campos
      setFormData({
        ...formData,
        address_street: dados.logradouro || formData.address_street,
        address_complement: dados.complemento || formData.address_complement,
        address_neighborhood: dados.bairro || formData.address_neighborhood,
        address_city: dados.localidade || formData.address_city,
        address_state: dados.uf || formData.address_state,
      })

      toast({
        title: 'Sucesso!',
        description: 'Endereço carregado automaticamente',
      })
    } catch (error: any) {
      toast({
        variant: 'destructive',
        title: 'Erro ao consultar CEP',
        description: error.response?.data?.detail || 'Não foi possível consultar o CEP',
      })
    } finally {
      setConsultingCEP(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Novo Cliente
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Novo Cliente</DialogTitle>
          <DialogDescription>
            Cadastre um novo cliente no sistema
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            {/* Tipo */}
            <div className="grid gap-2">
              <Label htmlFor="type">Tipo de Pessoa *</Label>
              <Select
                value={formData.type}
                onValueChange={(value) =>
                  setFormData({ ...formData, type: value, document: '' })
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecione o tipo" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="pf">Pessoa Física (PF)</SelectItem>
                  <SelectItem value="pj">Pessoa Jurídica (PJ)</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Informações Básicas */}
            <div className="grid gap-2">
              <Label htmlFor="name">
                {formData.type === 'pf' ? 'Nome Completo *' : 'Razão Social *'}
              </Label>
              <Input
                id="name"
                required
                value={formData.name}
                onChange={(e) =>
                  setFormData({ ...formData, name: e.target.value })
                }
                placeholder={
                  formData.type === 'pf'
                    ? 'João da Silva'
                    : 'Empresa XYZ Ltda'
                }
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="grid gap-2">
                <Label htmlFor="document">
                  {formData.type === 'pf' ? 'CPF *' : 'CNPJ *'}
                </Label>
                <div className="flex gap-2">
                  <div className="relative flex-1">
                    <Input
                      id="document"
                      required
                      value={formData.document}
                      onChange={(e) => handleDocumentChange(e.target.value)}
                      placeholder={
                        formData.type === 'pf' ? '000.000.000-00' : '00.000.000/0000-00'
                      }
                      maxLength={formData.type === 'pf' ? 14 : 18}
                      className={
                        documentoValido === false
                          ? 'border-red-500 focus-visible:ring-red-500'
                          : documentoValido === true
                          ? 'border-green-500 focus-visible:ring-green-500'
                          : ''
                      }
                    />
                    {documentoValido !== null && (
                      <div className="absolute right-2 top-1/2 -translate-y-1/2">
                        {documentoValido ? (
                          <span className="text-green-500 text-sm">✓</span>
                        ) : (
                          <span className="text-red-500 text-sm">✗</span>
                        )}
                      </div>
                    )}
                  </div>
                  {formData.type === 'pj' && (
                    <Button
                      type="button"
                      variant="outline"
                      size="icon"
                      onClick={consultarCNPJ}
                      disabled={consultingCNPJ || formData.document.replace(/\D/g, '').length !== 14 || documentoValido === false}
                      title="Consultar CNPJ na Receita Federal"
                    >
                      {consultingCNPJ ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <Search className="h-4 w-4" />
                      )}
                    </Button>
                  )}
                </div>
              </div>

              <div className="grid gap-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                  placeholder="email@exemplo.com"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="grid gap-2">
                <Label htmlFor="phone">Telefone</Label>
                <Input
                  id="phone"
                  value={formData.phone}
                  onChange={(e) =>
                    setFormData({ ...formData, phone: e.target.value })
                  }
                  placeholder="(11) 3333-3333"
                />
              </div>

              <div className="grid gap-2">
                <Label htmlFor="mobile">Celular</Label>
                <Input
                  id="mobile"
                  value={formData.mobile}
                  onChange={(e) =>
                    setFormData({ ...formData, mobile: e.target.value })
                  }
                  placeholder="(11) 99999-9999"
                />
              </div>
            </div>

            {/* Dados PJ */}
            {formData.type === 'pj' && (
              <div className="border-t pt-4 mt-2">
                <h3 className="text-sm font-medium mb-3">Dados da Empresa</h3>

                <div className="grid gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="trade_name">Nome Fantasia</Label>
                    <Input
                      id="trade_name"
                      value={formData.trade_name}
                      onChange={(e) =>
                        setFormData({ ...formData, trade_name: e.target.value })
                      }
                    />
                  </div>

                  <div className="grid gap-2">
                    <Label htmlFor="company_name">Razão Social Completa</Label>
                    <Input
                      id="company_name"
                      value={formData.company_name}
                      onChange={(e) =>
                        setFormData({ ...formData, company_name: e.target.value })
                      }
                    />
                  </div>

                  <div className="grid grid-cols-3 gap-4">
                    <div className="grid gap-2">
                      <Label htmlFor="cnae_primary">CNAE Principal</Label>
                      <Input
                        id="cnae_primary"
                        value={formData.cnae_primary}
                        onChange={(e) =>
                          setFormData({
                            ...formData,
                            cnae_primary: e.target.value,
                          })
                        }
                        placeholder="0000-0/00"
                      />
                    </div>

                    <div className="grid gap-2">
                      <Label htmlFor="state_registration">Inscrição Estadual</Label>
                      <Input
                        id="state_registration"
                        value={formData.state_registration}
                        onChange={(e) =>
                          setFormData({
                            ...formData,
                            state_registration: e.target.value,
                          })
                        }
                      />
                    </div>

                    <div className="grid gap-2">
                      <Label htmlFor="municipal_registration">
                        Inscrição Municipal
                      </Label>
                      <Input
                        id="municipal_registration"
                        value={formData.municipal_registration}
                        onChange={(e) =>
                          setFormData({
                            ...formData,
                            municipal_registration: e.target.value,
                          })
                        }
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Endereço */}
            <div className="border-t pt-4 mt-2">
              <h3 className="text-sm font-medium mb-3">Endereço (Opcional)</h3>

              <div className="grid gap-4">
                <div className="grid grid-cols-3 gap-4">
                  <div className="col-span-2 grid gap-2">
                    <Label htmlFor="address_street">Rua</Label>
                    <Input
                      id="address_street"
                      value={formData.address_street}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          address_street: e.target.value,
                        })
                      }
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="address_number">Número</Label>
                    <Input
                      id="address_number"
                      value={formData.address_number}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          address_number: e.target.value,
                        })
                      }
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="address_complement">Complemento</Label>
                    <Input
                      id="address_complement"
                      value={formData.address_complement}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          address_complement: e.target.value,
                        })
                      }
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="address_neighborhood">Bairro</Label>
                    <Input
                      id="address_neighborhood"
                      value={formData.address_neighborhood}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          address_neighborhood: e.target.value,
                        })
                      }
                    />
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="address_city">Cidade</Label>
                    <Input
                      id="address_city"
                      value={formData.address_city}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          address_city: e.target.value,
                        })
                      }
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="address_state">Estado</Label>
                    <Input
                      id="address_state"
                      value={formData.address_state}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          address_state: e.target.value.toUpperCase().slice(0, 2),
                        })
                      }
                      placeholder="SP"
                      maxLength={2}
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="address_zipcode">CEP</Label>
                    <div className="flex gap-2">
                      <Input
                        id="address_zipcode"
                        value={formData.address_zipcode}
                        onChange={(e) =>
                          setFormData({
                            ...formData,
                            address_zipcode: formatCEP(e.target.value),
                          })
                        }
                        placeholder="00000-000"
                        maxLength={9}
                      />
                      <Button
                        type="button"
                        variant="outline"
                        size="icon"
                        onClick={consultarCEP}
                        disabled={consultingCEP || formData.address_zipcode.replace(/\D/g, '').length !== 8}
                        title="Consultar CEP"
                      >
                        {consultingCEP ? (
                          <Loader2 className="h-4 w-4 animate-spin" />
                        ) : (
                          <Search className="h-4 w-4" />
                        )}
                      </Button>
                    </div>
                  </div>
                </div>
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
              {loading ? 'Criando...' : 'Criar Cliente'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
