'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { useToast } from '@/components/ui/use-toast';
import { Building2, FileText, XCircle, Loader2 } from 'lucide-react';

// ========================================
// TIPOS DE PROCESSO DISPONÍVEIS
// ========================================
const PROCESS_TYPES = [
  {
    id: 'abertura',
    title: 'Abertura de Empresa',
    description: 'Constituir nova empresa',
    icon: Building2,
    color: 'bg-blue-500',
    hasMultipleOptions: false,
    options: []
  },
  {
    id: 'alteracao',
    title: 'Alteração Contratual',
    description: 'Alterações diversas no contrato social',
    icon: FileText,
    color: 'bg-green-500',
    hasMultipleOptions: true,
    options: [
      { id: 'endereco', label: 'Alteração de Endereço', description: 'Mudança do endereço da sede' },
      { id: 'socios', label: 'Alteração de Quadro Societário', description: 'Inclusão, exclusão ou alteração de sócios' },
      { id: 'capital', label: 'Alteração de Capital Social', description: 'Aumento ou redução do capital' },
      { id: 'atividade', label: 'Alteração de Atividade', description: 'Inclusão ou exclusão de CNAEs' },
      { id: 'nome', label: 'Alteração de Nome Empresarial', description: 'Mudança da razão social ou nome fantasia' },
      { id: 'administracao', label: 'Alteração de Administração', description: 'Mudança de administradores/diretores' }
    ]
  },
  {
    id: 'distrato',
    title: 'Distrato Social (Encerramento)',
    description: 'Encerramento da empresa',
    icon: XCircle,
    color: 'bg-red-500',
    hasMultipleOptions: false,
    options: []
  }
];

// ========================================
// COMPONENTE PRINCIPAL
// ========================================
export default function AutomationPage() {
  const router = useRouter();
  const { toast } = useToast();

  // Estados
  const [selectedType, setSelectedType] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [clients, setClients] = useState([]);
  const [selectedClient, setSelectedClient] = useState('');
  const [processTitle, setProcessTitle] = useState('');
  const [processDescription, setProcessDescription] = useState('');
  const [priority, setPriority] = useState('normal');
  const [deadline, setDeadline] = useState('30');
  const [isLoading, setIsLoading] = useState(false);
  const [loadingClients, setLoadingClients] = useState(true);

  // ========================================
  // BUSCAR CLIENTES AO CARREGAR
  // ========================================
  useEffect(() => {
    fetchClients();
  }, []);

  const fetchClients = async () => {
    try {
      const token = localStorage.getItem('access_token');  // CORRIGIDO: usar 'access_token' padrão
      const response = await fetch('https://legia-backend.onrender.com/api/v1/clients/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setClients(data);
      }
    } catch (error) {
      console.error('Erro ao buscar clientes:', error);
      toast({
        title: 'Erro',
        description: 'Não foi possível carregar a lista de clientes',
        variant: 'destructive'
      });
    } finally {
      setLoadingClients(false);
    }
  };

  // ========================================
  // ABRIR MODAL AO CLICAR NO CARD
  // ========================================
  const handleCardClick = (type) => {
    setSelectedType(type);
    setSelectedOptions([]);
    setProcessTitle('');
    setProcessDescription('');
    setPriority('normal');
    setDeadline('30');
    setIsModalOpen(true);
  };

  // ========================================
  // TOGGLE OPÇÕES (CHECKBOXES)
  // ========================================
  const toggleOption = (optionId) => {
    setSelectedOptions(prev => {
      if (prev.includes(optionId)) {
        return prev.filter(id => id !== optionId);
      } else {
        return [...prev, optionId];
      }
    });
  };

  // ========================================
  // CRIAR PROCESSO + WORKFLOW
  // ========================================
  const handleConfirm = async () => {
    // Validações
    if (!selectedClient) {
      toast({
        title: 'Cliente obrigatório',
        description: 'Por favor, selecione um cliente',
        variant: 'destructive'
      });
      return;
    }

    if (!processTitle.trim()) {
      toast({
        title: 'Título obrigatório',
        description: 'Por favor, informe o título do processo',
        variant: 'destructive'
      });
      return;
    }

    if (selectedType.hasMultipleOptions && selectedOptions.length === 0) {
      toast({
        title: 'Seleção obrigatória',
        description: 'Por favor, selecione pelo menos uma alteração',
        variant: 'destructive'
      });
      return;
    }

    setIsLoading(true);

    try {
      const token = localStorage.getItem('access_token');  // CORRIGIDO: usar 'access_token' padrão

      // ========================================
      // PASSO 1: CRIAR PROCESSO
      // ========================================
      console.log('📝 Criando processo...');
      
      const processPayload = {
        client_id: parseInt(selectedClient),
        process_type: selectedType.id,
        title: processTitle,
        description: processDescription || `Processo de ${selectedType.title}`,
        priority: priority,
        deadline_days: parseInt(deadline),
        alteration_types: selectedOptions // Array de alterações selecionadas
      };

      console.log('Payload do processo:', processPayload);

      const processResponse = await fetch('https://legia-backend.onrender.com/api/v1/processes/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(processPayload)
      });

      if (!processResponse.ok) {
        const errorData = await processResponse.json();
        throw new Error(errorData.detail || 'Erro ao criar processo');
      }

      const process = await processResponse.json();
      console.log('✅ Processo criado:', process);

      // Validar que processo tem ID
      if (!process.id) {
        throw new Error('Processo criado sem ID válido');
      }

      // ========================================
      // PASSO 2: CRIAR WORKFLOW
      // ========================================
      console.log('⚙️ Criando workflow...');

      const workflowPayload = {
        process_id: process.id,
        workflow_type: selectedType.id
      };

      console.log('Payload do workflow:', workflowPayload);

      const workflowResponse = await fetch('https://legia-backend.onrender.com/api/v1/workflows/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(workflowPayload)
      });

      if (!workflowResponse.ok) {
        const errorData = await workflowResponse.json();
        throw new Error(errorData.detail || 'Erro ao criar workflow');
      }

      const workflow = await workflowResponse.json();
      console.log('✅ Workflow criado:', workflow);

      // Validar que workflow tem ID e stages
      if (!workflow.id) {
        throw new Error('Workflow criado sem ID válido');
      }

      if (!workflow.stages || workflow.stages.length === 0) {
        throw new Error('Workflow criado sem etapas');
      }

      // ========================================
      // SUCESSO: NAVEGAR PARA PÁGINA DO WORKFLOW
      // ========================================
      toast({
        title: 'Sucesso! 🎉',
        description: `Processo criado! Os agentes já começaram a trabalhar.`
      });

      // Fechar modal
      setIsModalOpen(false);

      // Aguardar 1 segundo e navegar
      setTimeout(() => {
        router.push(`/tenant/automation/${workflow.id}`);
      }, 1000);

    } catch (error) {
      console.error('❌ Erro completo:', error);
      
      toast({
        title: 'Erro ao criar processo',
        description: error.message || 'Verifique sua conexão e tente novamente',
        variant: 'destructive'
      });
    } finally {
      setIsLoading(false);
    }
  };

  // ========================================
  // CANCELAR MODAL
  // ========================================
  const handleCancel = () => {
    setIsModalOpen(false);
    setSelectedType(null);
    setSelectedOptions([]);
    setProcessTitle('');
    setProcessDescription('');
  };

  // ========================================
  // RENDER
  // ========================================
  return (
    <div className="container mx-auto py-8">
      {/* HEADER */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Automação de Processos</h1>
        <p className="text-muted-foreground">
          Inicie um processo totalmente automatizado. Os agentes trabalharão juntos para completar tudo!
        </p>
      </div>

      {/* CARDS DE TIPOS DE PROCESSO */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {PROCESS_TYPES.map((type) => {
          const Icon = type.icon;
          return (
            <Card
              key={type.id}
              className="cursor-pointer hover:shadow-lg transition-shadow"
              onClick={() => handleCardClick(type)}
            >
              <CardHeader>
                <div className={`w-16 h-16 rounded-lg ${type.color} flex items-center justify-center mb-4`}>
                  <Icon className="w-8 h-8 text-white" />
                </div>
                <CardTitle>{type.title}</CardTitle>
                <CardDescription>{type.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full">Selecionar</Button>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* MODAL DE CONFIGURAÇÃO */}
      <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{selectedType?.title}</DialogTitle>
            <DialogDescription>{selectedType?.description}</DialogDescription>
          </DialogHeader>

          <div className="space-y-6 py-4">
            {/* SELEÇÃO DE CLIENTE */}
            <div>
              <Label htmlFor="client">Cliente *</Label>
              <Select value={selectedClient} onValueChange={setSelectedClient}>
                <SelectTrigger>
                  <SelectValue placeholder={loadingClients ? "Carregando..." : "Selecione o cliente"} />
                </SelectTrigger>
                <SelectContent>
                  {clients.map((client) => (
                    <SelectItem key={client.id} value={client.id.toString()}>
                      {client.name} - {client.cpf_cnpj}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* OPÇÕES MÚLTIPLAS (SE APLICÁVEL) */}
            {selectedType?.hasMultipleOptions && (
              <div>
                <Label className="mb-3 block">Selecione as alterações *</Label>
                <div className="space-y-3">
                  {selectedType.options.map((option) => (
                    <div key={option.id} className="flex items-start space-x-3 p-3 border rounded-lg hover:bg-accent">
                      <Checkbox
                        id={option.id}
                        checked={selectedOptions.includes(option.id)}
                        onCheckedChange={() => toggleOption(option.id)}
                      />
                      <div className="flex-1">
                        <label
                          htmlFor={option.id}
                          className="font-medium cursor-pointer"
                        >
                          {option.label}
                        </label>
                        <p className="text-sm text-muted-foreground">
                          {option.description}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
                {selectedOptions.length > 0 && (
                  <p className="text-sm text-muted-foreground mt-2">
                    {selectedOptions.length} alteração(ões) selecionada(s)
                  </p>
                )}
              </div>
            )}

            {/* TÍTULO DO PROCESSO */}
            <div>
              <Label htmlFor="title">Título do Processo *</Label>
              <Input
                id="title"
                placeholder={`Ex: ${selectedType?.title} - Cliente XYZ`}
                value={processTitle}
                onChange={(e) => setProcessTitle(e.target.value)}
              />
            </div>

            {/* DESCRIÇÃO */}
            <div>
              <Label htmlFor="description">Descrição (opcional)</Label>
              <Textarea
                id="description"
                placeholder="Informações adicionais sobre o processo..."
                value={processDescription}
                onChange={(e) => setProcessDescription(e.target.value)}
                rows={3}
              />
            </div>

            {/* PRIORIDADE E PRAZO */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="priority">Prioridade</Label>
                <Select value={priority} onValueChange={setPriority}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="baixa">Baixa</SelectItem>
                    <SelectItem value="normal">Normal</SelectItem>
                    <SelectItem value="alta">Alta</SelectItem>
                    <SelectItem value="urgente">Urgente</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="deadline">Prazo (dias)</Label>
                <Input
                  id="deadline"
                  type="number"
                  min="1"
                  value={deadline}
                  onChange={(e) => setDeadline(e.target.value)}
                />
              </div>
            </div>
          </div>

          {/* BOTÕES */}
          <div className="flex justify-end space-x-3">
            <Button
              variant="outline"
              onClick={handleCancel}
              disabled={isLoading}
            >
              Cancelar
            </Button>
            <Button
              onClick={handleConfirm}
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Criando...
                </>
              ) : (
                'Iniciar Processo'
              )}
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
