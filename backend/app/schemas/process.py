"""
LEGIA PLATFORM - Schemas de Processos
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ProcessBase(BaseModel):
    """Base schema para Process"""
    client_id: int = Field(..., gt=0, description="ID do cliente")
    process_type: str = Field(..., description="Tipo: abertura, alteracao, encerramento, regularizacao")
    title: str = Field(..., min_length=3, max_length=200, description="Título do processo")
    description: Optional[str] = Field(None, description="Descrição detalhada")
    priority: Optional[str] = Field("normal", description="Prioridade: baixa, normal, alta")
    estimated_days: Optional[int] = Field(30, ge=1, description="Prazo estimado em dias")


class ProcessCreate(ProcessBase):
    """Schema para criar Process"""
    assigned_to: Optional[int] = Field(None, description="ID do usuário responsável")
    status: Optional[str] = Field("aguardando", description="Status inicial")


class ProcessUpdate(BaseModel):
    """Schema para atualizar Process"""
    client_id: Optional[int] = None
    process_type: Optional[str] = None
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field(
        None,
        description="Status: aguardando, em_andamento, protocolado, concluido, cancelado"
    )
    priority: Optional[str] = Field(None, description="Prioridade: baixa, normal, alta")
    estimated_days: Optional[int] = Field(None, ge=1)
    assigned_to: Optional[int] = None


class ProcessResponse(BaseModel):
    """Schema para resposta de Process"""
    id: int
    client_id: int
    client_name: Optional[str] = None
    client_document: Optional[str] = None
    process_type: str
    status: str
    title: str
    description: Optional[str] = None
    priority: str
    estimated_days: int
    assigned_to: Optional[int] = None
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProcessListResponse(BaseModel):
    """Schema para lista de Processes"""
    processes: List[ProcessResponse]
    total: int
    page: int
    per_page: int


class TimelineEvent(BaseModel):
    """Schema para evento de timeline"""
    id: int
    process_id: int
    event_type: str
    description: str
    metadata: Optional[Dict[str, Any]] = None
    created_by: Optional[int] = None
    user_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TimelineEventCreate(BaseModel):
    """Schema para criar evento de timeline"""
    event_type: str = Field(..., description="Tipo: created, status_changed, document_added, note, protocol")
    description: str = Field(..., min_length=3, description="Descrição do evento")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Dados adicionais em JSON")


class ProcessTimelineResponse(BaseModel):
    """Schema para timeline de um processo"""
    process_id: int
    events: List[TimelineEvent]


class ProcessStatsResponse(BaseModel):
    """Schema para estatísticas de processos"""
    total: int = 0
    aguardando: int = 0
    em_andamento: int = 0
    concluido: int = 0
    cancelado: int = 0
    alta_prioridade: int = 0
    tempo_medio_dias: Optional[float] = None
