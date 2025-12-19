'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Users, Folder, FileText, TrendingUp } from 'lucide-react'

export default function TenantDashboard() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">
          Visão geral do seu escritório
        </p>
      </div>

      {/* Métricas */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Total de Clientes
            </CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
            <p className="text-xs text-muted-foreground">
              Nenhum cliente cadastrado
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Processos Ativos
            </CardTitle>
            <Folder className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
            <p className="text-xs text-muted-foreground">
              Nenhum processo ativo
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Documentos
            </CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
            <p className="text-xs text-muted-foreground">
              Nenhum documento
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Taxa de Conclusão
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0%</div>
            <p className="text-xs text-muted-foreground">
              Sem dados
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Ações Rápidas */}
      <Card>
        <CardHeader>
          <CardTitle>Ações Rápidas</CardTitle>
          <CardDescription>
            Comece cadastrando seus primeiros dados
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <a
              href="/tenant/clients"
              className="p-6 border rounded-lg hover:bg-accent transition-colors text-center"
            >
              <Users className="h-8 w-8 mx-auto mb-2 text-primary" />
              <h3 className="font-medium">Cadastrar Cliente</h3>
              <p className="text-sm text-muted-foreground mt-1">
                Adicione um novo cliente
              </p>
            </a>

            <a
              href="/tenant/processes"
              className="p-6 border rounded-lg hover:bg-accent transition-colors text-center"
            >
              <Folder className="h-8 w-8 mx-auto mb-2 text-primary" />
              <h3 className="font-medium">Novo Processo</h3>
              <p className="text-sm text-muted-foreground mt-1">
                Inicie um processo
              </p>
            </a>

            <a
              href="/tenant/documents"
              className="p-6 border rounded-lg hover:bg-accent transition-colors text-center"
            >
              <FileText className="h-8 w-8 mx-auto mb-2 text-primary" />
              <h3 className="font-medium">Upload Documento</h3>
              <p className="text-sm text-muted-foreground mt-1">
                Envie documentos
              </p>
            </a>
          </div>
        </CardContent>
      </Card>

      {/* Processos Recentes */}
      <Card>
        <CardHeader>
          <CardTitle>Processos Recentes</CardTitle>
          <CardDescription>
            Últimos processos em andamento
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-muted-foreground">
            <Folder className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p>Nenhum processo cadastrado ainda</p>
            <p className="text-sm mt-2">
              Comece criando seu primeiro processo de legalização
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
