"""
LEGIA PLATFORM - Validadores
Validação de CPF e CNPJ conforme algoritmo oficial
"""


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
