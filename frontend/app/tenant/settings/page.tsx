'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Save, User, Building2, Bell } from 'lucide-react'
import { authService } from '@/lib/auth'

export default function SettingsPage() {
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    setUser(authService.getCurrentUser())
  }, [])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Configurações</h1>
        <p className="text-muted-foreground mt-1">
          Gerenciar configurações da conta e preferências
        </p>
      </div>

      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-5 w-5" />
              Perfil do Usuário
            </CardTitle>
            <CardDescription>
              Informações pessoais e credenciais
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label htmlFor="name">Nome</Label>
              <Input id="name" defaultValue={user?.name} />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" defaultValue={user?.email} disabled />
              <p className="text-xs text-muted-foreground">
                O email não pode ser alterado
              </p>
            </div>

            <div className="grid gap-2">
              <Label htmlFor="phone">Telefone</Label>
              <Input id="phone" defaultValue="" placeholder="(00) 00000-0000" />
            </div>

            <Button>
              <Save className="mr-2 h-4 w-4" />
              Salvar Alterações
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Building2 className="h-5 w-5" />
              Informações do Escritório
            </CardTitle>
            <CardDescription>
              Dados do seu escritório
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label htmlFor="office_name">Nome do Escritório</Label>
              <Input id="office_name" defaultValue={user?.tenant_name} />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="office_cnpj">CNPJ</Label>
              <Input id="office_cnpj" placeholder="00.000.000/0000-00" />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="office_address">Endereço</Label>
              <Input id="office_address" placeholder="Rua, Número, Complemento" />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="grid gap-2">
                <Label htmlFor="office_city">Cidade</Label>
                <Input id="office_city" />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="office_state">Estado</Label>
                <Input id="office_state" maxLength={2} />
              </div>
            </div>

            <Button>
              <Save className="mr-2 h-4 w-4" />
              Salvar Informações
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bell className="h-5 w-5" />
              Notificações
            </CardTitle>
            <CardDescription>
              Configurar preferências de notificações
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <Label>Email de processos</Label>
                <p className="text-sm text-muted-foreground">
                  Receber atualizações sobre processos por email
                </p>
              </div>
              <input type="checkbox" defaultChecked />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label>Email de vencimentos</Label>
                <p className="text-sm text-muted-foreground">
                  Alertas de documentos próximos ao vencimento
                </p>
              </div>
              <input type="checkbox" defaultChecked />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label>Email de novos clientes</Label>
                <p className="text-sm text-muted-foreground">
                  Notificação quando novos clientes forem cadastrados
                </p>
              </div>
              <input type="checkbox" defaultChecked />
            </div>

            <Button>
              <Save className="mr-2 h-4 w-4" />
              Salvar Preferências
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Segurança</CardTitle>
            <CardDescription>
              Alterar senha e configurações de segurança
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label htmlFor="current_password">Senha Atual</Label>
              <Input id="current_password" type="password" />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="new_password">Nova Senha</Label>
              <Input id="new_password" type="password" />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="confirm_password">Confirmar Nova Senha</Label>
              <Input id="confirm_password" type="password" />
            </div>

            <Button variant="secondary">
              Alterar Senha
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
