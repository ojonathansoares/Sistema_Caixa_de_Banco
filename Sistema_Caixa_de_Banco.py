def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Falha: valor inválido.")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Falha: saldo insuficiente.")

    elif excedeu_limite:
        print("Falha: o valor excede o limite por saque.")

    elif excedeu_saques:
        print("Falha: limite de saques diários atingido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")
    else:
        print("Falha: valor inválido.")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n========== EXTRATO ==========")
    print("Sem movimentações." if not extrato else extrato)
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("=============================\n")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")

    usuario_existente = next((u for u in usuarios if u["cpf"] == cpf), None)

    if usuario_existente:
        print("Usuário já cadastrado!")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (logradouro, nº - bairro - cidade/UF): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("Usuário criado com sucesso!")


def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")

    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)

    if not usuario:
        print("Usuário não encontrado. Crie o usuário primeiro.")
        return

    tipo = input("Tipo de conta ([C]orrente / [P]oupança): ").upper()

    if tipo not in ["C", "P"]:
        print("Tipo inválido.")
        return

    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario,
        "tipo": "Corrente" if tipo == "C" else "Poupança",
    }

    contas.append(conta)
    print("Conta criada com sucesso!")


def listar_contas(contas):
    cpf = input("Informe o CPF do usuário (somente números): ")

    contas_do_usuario = [c for c in contas if c["usuario"]["cpf"] == cpf]

    if not contas_do_usuario:
        print("Nenhuma conta encontrada para este CPF.")
        return

    print(f"\nContas vinculadas ao CPF {cpf}:\n")

    for conta in contas_do_usuario:
        linha = f"""
Agência:\t{conta['agencia']}
C/C:\t\t{conta['numero_conta']}
Titular:\t{conta['usuario']['nome']}
Tipo:\t\t{conta['tipo']}
"""
        print("=" * 100)
        print(linha)
        print("=" * 100)


saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

usuarios = []
contas = []
AGENCIA = "0001"
numero_conta = 1

menu = """
[1]\tDepositar
[2]\tSacar
[3]\tExtrato
[4]\tCriar usuário
[5]\tCriar conta
[6]\tListar Contas
[0]\tSair
=> """

while True:

    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Valor do depósito: "))
        saldo, extrato = depositar(saldo, valor, extrato)

    elif opcao == "2":
        valor = float(input("Valor do saque: "))
        saldo, extrato, numero_saques = sacar(
            saldo=saldo,
            valor=valor,
            extrato=extrato,
            limite=limite,
            numero_saques=numero_saques,
            limite_saques=LIMITE_SAQUES
        )

    elif opcao == "3":
        exibir_extrato(saldo, extrato=extrato)

    elif opcao == "4":
        criar_usuario(usuarios)

    elif opcao == "5":
        criar_conta(AGENCIA, numero_conta, usuarios, contas)
        numero_conta += 1
        
    elif opcao == "6":
        listar_contas(contas)

    elif opcao == "0":
        print("Saindo...")
        break

    else:
        print("Opção inválida.")
