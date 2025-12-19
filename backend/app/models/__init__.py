"""
LEGIA PLATFORM - Modelos SQLAlchemy
"""
# Importar todos os modelos aqui para facilitar uso
from app.models.public.tenant import Tenant
from app.models.public.plan import Plan
from app.models.public.subscription import Subscription
from app.models.public.payment import Payment
from app.models.public.legia_user import LegiaUser

# Modelos tenant (serão criados dinamicamente)
from app.models.tenant.user import TenantUser
from app.models.tenant.client import Client
from app.models.tenant.process import Process
from app.models.tenant.document import Document
from app.models.tenant.quote import Quote
from app.models.tenant.protocol import Protocol
from app.models.tenant.communication import Communication
from app.models.tenant.chat_message import ChatMessage

__all__ = [
    # Public schema
    "Tenant",
    "Plan",
    "Subscription",
    "Payment",
    "LegiaUser",
    # Tenant schema
    "TenantUser",
    "Client",
    "Process",
    "Document",
    "Quote",
    "Protocol",
    "Communication",
    "ChatMessage",
]
