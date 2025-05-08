def depositar(saldo, valor, historico_transacoes): #Renomeando aqui também
    """Realiza um depósito."""
    if valor > 0:
        saldo += valor
        historico_transacoes += f"Depósito: R$ {valor:.2f}\n"
        return saldo, historico_transacoes
    else:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, historico_transacoes


def sacar(**kwargs):
    """Realiza um saque."""
    saldo = kwargs["saldo"]
    valor = kwargs["valor"]
    historico_transacoes = kwargs["historico_transacoes"] # Renomeado
    limite = kwargs["limite"]
    numero_saques = kwargs["numero_saques"]
    limite_saques = kwargs["limite_saques"]

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        return None #retorna None explicitamente
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
        return None #retorna None explicitamente
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
        return None #retorna None explicitamente
    elif valor > 0:
        saldo -= valor
        historico_transacoes += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        return saldo, historico_transacoes, numero_saques
    else:
        print("Operação falhou! O valor informado é inválido.")
        return None #retorna None explicitamente


def extrato(saldo, *, historico_transacoes): # Renomeado aqui também
    """Imprime o extrato da conta."""
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not historico_transacoes else historico_transacoes)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def cadastrar_usuario(usuarios):
    """Cadastra um novo usuário."""
    while True:
        cpf = input("Digite o CPF (somente números): ")
        if not cpf.isdigit() or len(cpf) != 11:
            print("CPF inválido. Digite apenas números e 11 dígitos.")
            continue
        if any(u["cpf"] == cpf for u in usuarios):
            print("CPF já cadastrado.")
            continue
        break

    nome = input("Digite o nome: ")
    data_nascimento = input("Digite a data de nascimento (DD/MM/AAAA): ")
    endereco = input(
        "Digite o endereço (Logradouro, nro - Bairro - Cidade/Sigla Estado): "
    )
    usuarios.append(
        {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "endereco": endereco,
        }
    )
    print("Usuário cadastrado com sucesso!")


def cadastrar_conta(contas, usuarios):
    """Cadastra uma nova conta corrente."""
    while True:
        cpf = input("Digite o CPF do usuário: ")
        usuario = next((u for u in usuarios if u["cpf"] == cpf), None)
        if usuario is None:
            print("Usuário não encontrado.")
            continue
        break

    numero_conta = len(contas) + 1
    contas.append(
        {"agencia": "0001", "numero": numero_conta, "usuario": usuario}
    )
    print("Conta corrente criada com sucesso!")


def listar_contas(contas):
    """Lista todas as contas cadastradas."""
    if not contas:
        print("Não há contas cadastradas.")
        return

    print("\nLista de Contas:")
    for conta in contas:
        print(
            f"Agência: {conta['agencia']}, Número: {conta['numero']}, Usuário: {conta['usuario']['nome']}"
        )

usuarios = []
contas = []
saldo = 0
limite = 500
historico_transacoes = "" 
numero_saques = 0
LIMITE_SAQUES = 3

menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[u] Cadastrar Usuário
[c] Cadastrar Conta
[l] Listar Contas
[q] Sair

=> """


while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        saldo, historico_transacoes = depositar(saldo, valor, historico_transacoes) # Atualizando historico_transacoes

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        resultado_saque = sacar(
            saldo=saldo,
            valor=valor,
            historico_transacoes=historico_transacoes,
            limite=limite,
            numero_saques=numero_saques,
            limite_saques=LIMITE_SAQUES,
        )
        if resultado_saque:
            saldo, historico_transacoes, numero_saques = resultado_saque

    elif opcao == "e":
        extrato(saldo, historico_transacoes=historico_transacoes)


    elif opcao == "u":
        cadastrar_usuario(usuarios)

    elif opcao == "c":
        cadastrar_conta(contas, usuarios)

    elif opcao == "l":
        listar_contas(contas)

    elif opcao == "q":
        break

    else:
        print(
            "Operação inválida, por favor selecione novamente a operação desejada."
        )