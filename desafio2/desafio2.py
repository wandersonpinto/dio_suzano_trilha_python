from datetime import datetime

class ContaBancaria:
    def __init__(self, numero_conta):
        self.numero_conta = numero_conta
        self.saldo = 0
        self.historico = []  # Lista para armazenar todas as transações
        self.saques_diarios = 0
        self.ultimo_dia_saque = None

    def deposito(self, valor):
        if valor > 0:
            self.saldo += valor
            self.historico.append((datetime.now(), "Depósito", valor))
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso. Novo saldo: R$ {self.saldo:.2f}")
        else:
            print("Valor de depósito inválido. O valor deve ser positivo.")

    def saque(self, valor):
        hoje = datetime.now().date()
        if self.ultimo_dia_saque is None or self.ultimo_dia_saque < hoje:
            self.saques_diarios = 0
            self.ultimo_dia_saque = hoje

        if self.saques_diarios < 3:
            if 0 < valor <= 500 and valor <= self.saldo:
                self.saldo -= valor
                self.historico.append((datetime.now(), "Saque", valor))
                self.saques_diarios += 1
                print(f"Saque de R$ {valor:.2f} realizado com sucesso. Novo saldo: R$ {self.saldo:.2f}")
            else:
                print("Valor de saque inválido (limite diário de R$ 500,00 ou saldo insuficiente).")
        else:
            print("Limite de 3 saques diários atingido.")

    def extrato(self):
        print("\nEXTRATO:")
        print(f"Número da conta: {self.numero_conta}")
        print(f"Saldo atual: R$ {self.saldo:.2f}")
        if self.historico:
            print("\nHistórico de Transações:")
            for data, tipo, valor in self.historico:
                print(f"{data.strftime('%d/%m/%Y %H:%M:%S')} - {tipo}: R$ {valor:.2f}")
        else:
            print("\nNão há transações registradas.")

class Banco:
    def __init__(self, telefones, contas, nomes, sobrenomes):
        if not (len(telefones) == len(contas) == len(nomes) == len(sobrenomes)):
            raise ValueError("As listas devem ter o mesmo tamanho.")

        # Criando um dicionário para acesso mais eficiente pelo telefone
        self.dados_correntistas = dict(zip(telefones, zip(contas, nomes, sobrenomes)))


    def get_dados_conta(self, telefone):
        try:
            conta, nome, sobrenome = self.dados_correntistas[telefone]
            return conta, nome, sobrenome
        except KeyError:
            return None

    def processa_entrada_usuario(self):
        while True:
            numero_telefone = input("Digite o número de telefone: ")
            dados_conta = self.get_dados_conta(numero_telefone)
            if dados_conta:
                return dados_conta
            else:
                print("Número de telefone não encontrado. Tente novamente.")


def main():
    telefones = ["27996", "27997", "27998"]
    contas = ["1000-1", "1001-0", "1002-2"]
    nomes = ["João", "Wanderson", "Leonardo"]
    sobrenomes = ["Carlos", "Pereira", "Patrick"]

    banco = Banco(telefones, contas, nomes, sobrenomes)
    dados_conta = banco.processa_entrada_usuario()

    if dados_conta:
        conta, nome, sobrenome = dados_conta
        print(f"\nDados do correntista:")
        print(f"Nome: {nome} {sobrenome}")
        print(f"Conta: {conta}")

        conta_bancaria = ContaBancaria(conta)  # Cria a conta bancária

        while True:
            print("\nEscolha uma opção:")
            print("1. Depósito")
            print("2. Saque")
            print("3. Extrato")
            print("4. Sair")

            opcao = input("Sua escolha: ")

            if opcao == '1':
                valor = float(input("Digite o valor a depositar: "))
                conta_bancaria.deposito(valor)
            elif opcao == '2':
                valor = float(input("Digite o valor a sacar: "))
                conta_bancaria.saque(valor)
            elif opcao == '3':
                conta_bancaria.extrato()
            elif opcao == '4':
                print("Encerrando o programa.")
                break
            else:
                print("Opção inválida. Tente novamente.")
    else:
        print("\nNúmero de telefone inválido ou não encontrado.")


if __name__ == "__main__":
    main()