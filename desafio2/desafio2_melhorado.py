import csv
from datetime import datetime, date
import os

class ContaBancaria:
    def __init__(self, numero_conta, nome_arquivo_extrato="C:\desenvolvimento\projetos\dio_suzano_trilha_python\desafio2\extrato.csv"):
            self.numero_conta = numero_conta
            self.nome_arquivo_extrato = nome_arquivo_extrato 
            self.saldo = self.carregar_saldo_inicial()
            self.historico = []
            self.saques_diarios = 0
            self.ultimo_dia_saque = None

    def carregar_saldo_inicial(self):
        try:
            with open(self.nome_arquivo_extrato, 'r', newline='', encoding='utf-8') as arquivo_csv:
                leitor = csv.DictReader(arquivo_csv, delimiter=';')
                saldo_final = 0
                for linha in leitor:
                    valor = float(linha['Valor'])
                    if linha['Descrição'] == "Depósito":
                        saldo_final += valor
                    else:
                        saldo_final -= valor
                return saldo_final
        except FileNotFoundError:
            return 0
        except Exception as e:
            print(f"Erro ao ler saldo inicial do extrato: {e}")
            return 0


    def deposito(self, valor):
        if valor > 0:
            self.saldo += valor
            self.adiciona_transacao("Depósito", valor)
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        else:
            print("Valor de depósito inválido. O valor deve ser positivo.")

    def saque(self, valor):
        hoje = datetime.now().date()
        if self.ultimo_dia_saque is None or self.ultimo_dia_saque < hoje:
            self.saques_diarios = 0
            self.ultimo_dia_saque = hoje

        if self.saques_diarios < 10:
            if 0 < valor <= 500 and valor <= self.saldo:
                self.saldo -= valor
                self.adiciona_transacao("Saque", valor)
                self.saques_diarios += 1
                print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
            else:
                print("Valor de saque inválido (limite diário de R$ 500,00 ou saldo insuficiente).")
        else:
            print("Limite de 10 saques diários atingido.")

    def adiciona_transacao(self, descricao, valor):
        data_hora = datetime.now()
        self.historico.append((data_hora, descricao, valor))
        self.grava_extrato()

    def grava_extrato(self):
        try:
            with open(self.nome_arquivo_extrato, 'a', newline='', encoding='utf-8') as arquivo_csv:
                escritor_csv = csv.writer(arquivo_csv, delimiter=';')
                if os.stat(self.nome_arquivo_extrato).st_size == 0:
                    escritor_csv.writerow(["Conta", "Data", "Descrição", "Valor"])
                for data_hora, descricao, valor in self.historico:
                    escritor_csv.writerow([self.numero_conta, data_hora.strftime("%d/%m/%Y %H:%M:%S"), descricao, valor])
        except FileNotFoundError:
            print(f"Arquivo '{self.nome_arquivo_extrato}' não encontrado. Criando um novo...")
            self.grava_extrato()
        except Exception as e:
            print(f"Erro ao gravar extrato no arquivo: {e}")

    def extrato(self):
        print("\nEXTRATO:")
        print(f"Número da conta: {self.numero_conta}")
        hoje = date.today()
        try:
            with open(self.nome_arquivo_extrato, 'r', newline='', encoding='utf-8') as arquivo_csv:
                leitor = csv.DictReader(arquivo_csv, delimiter=';')
                saldo = 0
                print("\nHistórico de Transações:")
                for linha in leitor:
                    data_transacao = datetime.strptime(linha['Data'], '%d/%m/%Y %H:%M:%S').date()
                    if data_transacao == hoje and linha['Conta'] == self.numero_conta:
                        descricao = linha['Descrição']
                        valor = float(linha['Valor'])
                        print(f"{linha['Data']} - {descricao}: R$ {valor:.2f}")
                        if descricao == "Depósito":
                            saldo += valor
                        else:
                            saldo -= valor
                print(f"\nSaldo atual: R$ {saldo:.2f}")
        except FileNotFoundError:
            print("Arquivo de extrato não encontrado.")
        except Exception as e:
            print(f"Erro ao ler o extrato: {e}")

class Banco:
    def __init__(self, nome_arquivo_clientes):
        self.clientes = self.carregar_clientes_csv(nome_arquivo_clientes)
        if self.clientes is None:
            print("Erro ao carregar clientes. O sistema encerrará.")
            exit() #Sai do programa se houver erro ao carregar os clientes

        # Criando um dicionário para acesso mais eficiente pelo telefone
        self.dados_correntistas = {telefone: (conta, nome, sobrenome) for telefone, conta, nome, sobrenome in self.clientes}


    def carregar_clientes_csv(self, nome_arquivo):
        clientes = []
        try:
            with open(nome_arquivo, 'r', newline='', encoding='utf-8') as arquivo_csv:
                leitor_csv = csv.reader(arquivo_csv, delimiter=',')
                next(leitor_csv)  # Pula a primeira linha (cabeçalho) se existir
                for linha in leitor_csv:
                    telefone, conta, nome, sobrenome = linha
                    clientes.append((telefone, conta, nome, sobrenome))
        except FileNotFoundError:
            print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
            return None
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return None
        return clientes


    def get_dados_conta(self, telefone):
        try:
            return self.dados_correntistas[telefone]
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
    nome_arquivo_clientes = "C:\desenvolvimento\projetos\dio_suzano_trilha_python\desafio2\clientes.csv" 

    banco = Banco(nome_arquivo_clientes)

    dados_conta = banco.processa_entrada_usuario()

    if dados_conta:
        conta, nome, sobrenome = dados_conta
        print(f"\nDados do correntista:")
        print(f"Nome: {nome} {sobrenome}")
        print(f"Conta: {conta}")

        conta_bancaria = ContaBancaria(conta)

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