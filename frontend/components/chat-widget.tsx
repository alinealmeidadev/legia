'use client'

import { useState, useEffect, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import api from '@/lib/api'
import { MessageCircle, X, Send, Loader2, Bot, User } from 'lucide-react'

interface Message {
  id: string
  role: 'user' | 'agent'
  content: string
  agent?: string
  timestamp: Date
}

export function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Scroll para última mensagem
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Mensagem de boas-vindas
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const welcomeMessage: Message = {
        id: '0',
        role: 'agent',
        content: 'Olá! 👋 Sou o assistente do LEG.Agents. Como posso te ajudar hoje?',
        agent: 'assistente',
        timestamp: new Date()
      }
      setMessages([welcomeMessage])
    }
  }, [isOpen, messages.length])

  const sendMessage = async () => {
    if (!inputMessage.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await api.post('/agents/chat', {
        message: inputMessage,
        context: {
          conversation_history: messages.slice(-5) // Últimas 5 mensagens
        }
      })

      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'agent',
        content: response.data.response,
        agent: response.data.agent,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, agentMessage])
    } catch (error: any) {
      console.error('Erro ao enviar mensagem:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'agent',
        content: 'Desculpe, ocorreu um erro. Por favor, tente novamente.',
        agent: 'sistema',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const getAgentIcon = (agent?: string) => {
    switch (agent) {
      case 'comercial':
        return '💼'
      case 'assistente':
        return '🙋'
      case 'legalizacao':
        return '🤖'
      default:
        return '🤖'
    }
  }

  const getAgentName = (agent?: string) => {
    const names: any = {
      comercial: 'Comercial',
      assistente: 'Assistente',
      legalizacao: 'Legalização',
      orquestrador: 'Orquestrador'
    }
    return names[agent || ''] || 'Assistente'
  }

  return (
    <>
      {/* Botão Flutuante */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 h-14 w-14 rounded-full bg-primary text-primary-foreground shadow-lg hover:scale-110 transition-transform duration-200 flex items-center justify-center z-50"
        >
          <MessageCircle className="h-6 w-6" />
          <span className="absolute -top-1 -right-1 h-5 w-5 rounded-full bg-red-500 text-white text-xs flex items-center justify-center animate-pulse">
            !
          </span>
        </button>
      )}

      {/* Widget de Chat */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-96 h-[600px] flex flex-col shadow-2xl rounded-lg overflow-hidden z-50 bg-background border">
          {/* Header */}
          <div className="bg-primary text-primary-foreground p-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-full bg-primary-foreground/20 flex items-center justify-center">
                <Bot className="h-5 w-5" />
              </div>
              <div>
                <h3 className="font-semibold">LEG.Agents</h3>
                <p className="text-xs opacity-90">Online agora</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsOpen(false)}
              className="hover:bg-primary-foreground/20"
            >
              <X className="h-5 w-5" />
            </Button>
          </div>

          {/* Mensagens */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-accent/5">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-[80%] ${
                    message.role === 'user' ? 'order-1' : 'order-2'
                  }`}
                >
                  {message.role === 'agent' && (
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-sm">{getAgentIcon(message.agent)}</span>
                      <Badge variant="secondary" className="text-xs">
                        {getAgentName(message.agent)}
                      </Badge>
                    </div>
                  )}
                  <div
                    className={`rounded-2xl px-4 py-2 ${
                      message.role === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted'
                    }`}
                  >
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    <p className="text-xs opacity-70 mt-1">
                      {message.timestamp.toLocaleTimeString('pt-BR', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </p>
                  </div>
                </div>
                <div
                  className={`flex-shrink-0 ${
                    message.role === 'user' ? 'order-2 ml-2' : 'order-1 mr-2'
                  }`}
                >
                  <div
                    className={`h-8 w-8 rounded-full flex items-center justify-center ${
                      message.role === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted'
                    }`}
                  >
                    {message.role === 'user' ? (
                      <User className="h-4 w-4" />
                    ) : (
                      <span className="text-sm">{getAgentIcon(message.agent)}</span>
                    )}
                  </div>
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-muted rounded-2xl px-4 py-2 flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span className="text-sm">Digitando...</span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t bg-background">
            <div className="flex gap-2">
              <Input
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Digite sua mensagem..."
                disabled={isLoading}
                className="flex-1"
              />
              <Button
                onClick={sendMessage}
                disabled={isLoading || !inputMessage.trim()}
                size="icon"
              >
                {isLoading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Send className="h-4 w-4" />
                )}
              </Button>
            </div>
            <p className="text-xs text-muted-foreground mt-2 text-center">
              Powered by LEG.Agents IA
            </p>
          </div>
        </div>
      )}
    </>
  )
}
