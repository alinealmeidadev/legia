"""
LEGIA PLATFORM - Modelo Payment (Pagamento)
Schema: public
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.base import Base


class Payment(Base):
    """
    Modelo Payment - Representa um pagamento de assinatura

    Integrado com Asaas para processamento de pagamentos
    """

    __tablename__ = "payments"
    __table_args__ = {"schema": "public"}

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("public.tenants.id"), nullable=False,
                      index=True)
    subscription_id = Column(Integer, ForeignKey("public.subscriptions.id"),
                            nullable=True)

    # Valores
    amount = Column(Numeric(10, 2), nullable=False, comment="Valor do pagamento")
    currency = Column(String(3), default="BRL", comment="Moeda")

    # Status
    status = Column(String(50), nullable=False, default="pending", index=True,
                   comment="Status: pending, paid, failed, refunded, canceled")

    # Método de pagamento
    payment_method = Column(String(50), nullable=False,
                           comment="Método: credit_card, boleto, pix")

    # Datas
    due_date = Column(Date, nullable=False, comment="Data de vencimento")
    paid_at = Column(DateTime, nullable=True, comment="Data de pagamento")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Gateway (Asaas)
    gateway_id = Column(String(255), nullable=True, index=True,
                       comment="ID do pagamento no Asaas")
    gateway_status = Column(String(100), nullable=True,
                           comment="Status retornado pelo gateway")
    invoice_url = Column(String(500), nullable=True,
                        comment="URL da fatura")
    boleto_url = Column(String(500), nullable=True,
                       comment="URL do boleto (se aplicável)")
    pix_qrcode = Column(Text, nullable=True,
                       comment="QR Code PIX (se aplicável)")

    # Detalhes do cartão (apenas últimos 4 dígitos)
    card_last4 = Column(String(4), nullable=True,
                       comment="Últimos 4 dígitos do cartão")
    card_brand = Column(String(20), nullable=True,
                       comment="Bandeira do cartão")

    # Falhas
    failure_code = Column(String(50), nullable=True,
                         comment="Código de erro (se falhou)")
    failure_message = Column(Text, nullable=True,
                            comment="Mensagem de erro")
    retry_count = Column(Integer, default=0,
                        comment="Número de tentativas de cobrança")

    # Extra Data
    extra_data = Column(JSON, default={},
                       comment="Dados adicionais em JSON")

    # Relacionamentos
    tenant = relationship("Tenant", back_populates="payments")
    subscription = relationship("Subscription", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.id}: Tenant {self.tenant_id} - R$ {self.amount} ({self.status})>"

    @property
    def is_paid(self) -> bool:
        """Verifica se o pagamento foi realizado"""
        return self.status == "paid"

    @property
    def is_pending(self) -> bool:
        """Verifica se está pendente"""
        return self.status == "pending"

    @property
    def is_failed(self) -> bool:
        """Verifica se falhou"""
        return self.status == "failed"

    @property
    def is_overdue(self) -> bool:
        """Verifica se está vencido"""
        if self.status != "pending":
            return False
        return date.today() > self.due_date

    @property
    def payment_method_display(self) -> str:
        """Retorna nome amigável do método de pagamento"""
        methods = {
            "credit_card": "Cartão de Crédito",
            "boleto": "Boleto Bancário",
            "pix": "PIX"
        }
        return methods.get(self.payment_method, self.payment_method)
