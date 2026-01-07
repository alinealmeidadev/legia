"""
LEGIA PLATFORM - Validadores
Validação de CPF, CNPJ, Email, Senha, Telefone e Sanitização
"""
import re
from typing import Optional, Tuple


def validar_cpf(cpf: str) -> bool:
    """
    Valida CPF usando o algoritmo oficial

    Args:
        cpf: CPF (com ou sem formatação)

    Returns:
        True se válido, False caso contrário
    """
    # Limpar CPF (remover caracteres não numéricos)
    cpf_limpo = ''.join(filter(str.isdigit, cpf))

    # Verificar se tem 11 dígitos
    if len(cpf_limpo) != 11:
        return False

    # Verificar se todos os dígitos são iguais (casos inválidos conhecidos)
    if cpf_limpo == cpf_limpo[0] * 11:
        return False

    # Calcular primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf_limpo[i]) * (10 - i)

    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    # Verificar primeiro dígito
    if int(cpf_limpo[9]) != digito1:
        return False

    # Calcular segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf_limpo[i]) * (11 - i)

    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    # Verificar segundo dígito
    if int(cpf_limpo[10]) != digito2:
        return False

    return True


def validar_cnpj(cnpj: str) -> bool:
    """
    Valida CNPJ usando o algoritmo oficial

    Args:
        cnpj: CNPJ (com ou sem formatação)

    Returns:
        True se válido, False caso contrário
    """
    # Limpar CNPJ (remover caracteres não numéricos)
    cnpj_limpo = ''.join(filter(str.isdigit, cnpj))

    # Verificar se tem 14 dígitos
    if len(cnpj_limpo) != 14:
        return False

    # Verificar se todos os dígitos são iguais (casos inválidos conhecidos)
    if cnpj_limpo == cnpj_limpo[0] * 14:
        return False

    # Calcular primeiro dígito verificador
    multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = 0
    for i in range(12):
        soma += int(cnpj_limpo[i]) * multiplicadores1[i]

    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    # Verificar primeiro dígito
    if int(cnpj_limpo[12]) != digito1:
        return False

    # Calcular segundo dígito verificador
    multiplicadores2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = 0
    for i in range(13):
        soma += int(cnpj_limpo[i]) * multiplicadores2[i]

    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    # Verificar segundo dígito
    if int(cnpj_limpo[13]) != digito2:
        return False

    return True


def formatar_cpf(cpf: str) -> str:
    """Formata CPF para XXX.XXX.XXX-XX"""
    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    if len(cpf_limpo) != 11:
        return cpf
    return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"


def formatar_cnpj(cnpj: str) -> str:
    """Formata CNPJ para XX.XXX.XXX/XXXX-XX"""
    cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj_limpo) != 14:
        return cnpj
    return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"


def validate_email(email: str) -> bool:
    """
    Valida formato de email

    Args:
        email: Email a ser validado

    Returns:
        True se válido, False caso contrário
    """
    if not email:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password_strength(password: str) -> Tuple[bool, Optional[str]]:
    """
    Valida força da senha

    Requisitos:
    - Mínimo 8 caracteres
    - Pelo menos 1 letra maiúscula
    - Pelo menos 1 letra minúscula
    - Pelo menos 1 número
    - Pelo menos 1 caractere especial

    Args:
        password: Senha a ser validada

    Returns:
        Tupla (is_valid, error_message)
    """
    if not password:
        return False, "Senha não pode estar vazia"

    if len(password) < 8:
        return False, "Senha deve ter no mínimo 8 caracteres"

    if not re.search(r'[A-Z]', password):
        return False, "Senha deve conter pelo menos uma letra maiúscula"

    if not re.search(r'[a-z]', password):
        return False, "Senha deve conter pelo menos uma letra minúscula"

    if not re.search(r'\d', password):
        return False, "Senha deve conter pelo menos um número"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Senha deve conter pelo menos um caractere especial"

    return True, None


def validate_phone(phone: str) -> bool:
    """
    Valida telefone brasileiro (com ou sem formatação)

    Aceita:
    - Fixo: (11) 3333-4444
    - Celular: (11) 99999-8888
    - Com código do país: +55 11 99999-8888

    Args:
        phone: Telefone a ser validado

    Returns:
        True se válido, False caso contrário
    """
    if not phone:
        return False

    # Remove formatação
    phone_clean = re.sub(r'[^0-9]', '', phone)

    # Remove código do país se presente (+55)
    if phone_clean.startswith('55') and len(phone_clean) > 11:
        phone_clean = phone_clean[2:]

    # Verifica se tem 10 ou 11 dígitos (fixo ou celular)
    if len(phone_clean) not in [10, 11]:
        return False

    # Verifica se DDD é válido (11-99)
    try:
        ddd = int(phone_clean[:2])
        if ddd < 11 or ddd > 99:
            return False
    except ValueError:
        return False

    return True


def sanitize_string(value: str, max_length: int = 500) -> str:
    """
    Sanitiza string removendo caracteres perigosos

    Remove:
    - Tags HTML
    - Caracteres de controle
    - SQL injection patterns básicos

    Args:
        value: String a ser sanitizada
        max_length: Tamanho máximo permitido

    Returns:
        String sanitizada
    """
    if not value:
        return ""

    # Limita tamanho
    value = value[:max_length]

    # Remove tags HTML
    value = re.sub(r'<[^>]*>', '', value)

    # Remove caracteres de controle
    value = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)

    # Remove padrões SQL básicos (proteção adicional ao SQLAlchemy)
    dangerous_patterns = [
        r'(\bDROP\b|\bDELETE\b|\bTRUNCATE\b|\bEXEC\b|\bEXECUTE\b)',
        r'(--|;|/\*|\*/)',
        r'(\bUNION\b.*\bSELECT\b)',
    ]

    for pattern in dangerous_patterns:
        value = re.sub(pattern, '', value, flags=re.IGNORECASE)

    return value.strip()


def validate_subdomain(subdomain: str) -> Tuple[bool, Optional[str]]:
    """
    Valida formato de subdomínio

    Requisitos:
    - Apenas letras minúsculas, números e hífens
    - Não pode começar ou terminar com hífen
    - Entre 3 e 50 caracteres

    Args:
        subdomain: Subdomínio a ser validado

    Returns:
        Tupla (is_valid, error_message)
    """
    if not subdomain:
        return False, "Subdomínio não pode estar vazio"

    if len(subdomain) < 3:
        return False, "Subdomínio deve ter no mínimo 3 caracteres"

    if len(subdomain) > 50:
        return False, "Subdomínio deve ter no máximo 50 caracteres"

    if not re.match(r'^[a-z0-9-]+$', subdomain):
        return False, "Subdomínio deve conter apenas letras minúsculas, números e hífens"

    if subdomain.startswith('-') or subdomain.endswith('-'):
        return False, "Subdomínio não pode começar ou terminar com hífen"

    # Subdomínios reservados
    reserved = ['admin', 'api', 'www', 'mail', 'ftp', 'localhost', 'legia', 'system']
    if subdomain in reserved:
        return False, f"Subdomínio '{subdomain}' é reservado"

    return True, None
