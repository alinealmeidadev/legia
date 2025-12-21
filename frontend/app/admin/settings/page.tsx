'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Settings, Save } from 'lucide-react'

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Configurações</h1>
        <p className="text-muted-foreground mt-1">
          Configurações gerais do sistema
        </p>
      </div>

      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Configurações Gerais</CardTitle>
            <CardDescription>
              Configurações básicas da plataforma
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label htmlFor="platform_name">Nome da Plataforma</Label>
              <Input id="platform_name" defaultValue="LEGIA" />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="support_email">Email de Suporte</Label>
              <Input id="support_email" type="email" defaultValue="suporte@legia.com.br" />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="contact_phone">Telefone de Contato</Label>
              <Input id="contact_phone" defaultValue="(11) 0000-0000" />
            </div>

            <Button>
              <Save className="mr-2 h-4 w-4" />
              Salvar Configurações
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Integrações</CardTitle>
            <CardDescription>
              Configurar integrações externas
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label htmlFor="google_api_key">Google API Key</Label>
              <Input id="google_api_key" type="password" placeholder="••••••••••••" />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="asaas_api_key">Asaas API Key (Sandbox)</Label>
              <Input id="asaas_api_key" type="password" placeholder="••••••••••••" />
            </div>

            <Button>
              <Save className="mr-2 h-4 w-4" />
              Salvar Integrações
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Notificações</CardTitle>
            <CardDescription>
              Configurar notificações do sistema
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <Label>Email de novos cadastros</Label>
                <p className="text-sm text-muted-foreground">
                  Receber email quando novos tenants se cadastrarem
                </p>
              </div>
              <input type="checkbox" defaultChecked />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label>Email de erros críticos</Label>
                <p className="text-sm text-muted-foreground">
                  Receber email quando ocorrerem erros críticos
                </p>
              </div>
              <input type="checkbox" defaultChecked />
            </div>

            <Button>
              <Save className="mr-2 h-4 w-4" />
              Salvar Notificações
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
