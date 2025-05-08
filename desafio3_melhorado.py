import csv
from datetime import datetime, date
import os

def get_filepath(filename):
    """Retorna o caminho completo para um arquivo, criando os diretórios se necessário"""
    filepath = os.path.join("dados", filename)  # Caminho relativo à pasta "dados"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    return filepath

class ContaBancaria:
    def __init__(self, numero_conta, agencia, usuario_cpf):
        self.numero_conta = numero_conta
        self.agencia = agencia
        self.usuario_cpf = usuario_cpf
        self.extrato_filepath = get_filepath(f"extrato_{numero_conta}.csv")
        self.saldo = self.carregar_saldo_inicial()
        self.historico = []
        self.saques_diarios = 0
        self.ultimo_dia_saque = None

    def carregar_saldo_inicial(self):
        try:
            with open(self.extrato_filepath, 'r', newline='', encoding='utf-8') as arquivo_csv:
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
            with open(self.extrato_filepath, 'a', newline='', encoding='utf-8') as arquivo_csv:
                escritor_csv = csv.writer(arquivo_csv, delimiter=';')
                if os.stat(self.extrato_filepath).st_size == 0:
                    escritor_csv.writerow(["Agência", "Conta", "Data", "Descrição", "Valor"])
                for data_hora, descricao, valor in self.historico:
                    escritor_csv.writerow([self.agencia, self.numero_conta, data_hora.strftime("%d/%m/%Y %H:%M:%S"), descricao, valor])
        except FileNotFoundError:
            print(f"Arquivo '{self.extrato_filepath}' não encontrado. Criando um novo...")
            self.grava_extrato()
        except Exception as e:
            print(f"Erro ao gravar extrato no arquivo: {e}")

    def extrato(self):
        print("\nEXTRATO:")
        print(f"Agência: {self.agencia}, Número da conta: {self.numero_conta}")
        try:
            with open(self.extrato_filepath, 'r', newline='', encoding='utf-8') as arquivo_csv:
                leitor = csv.DictReader(arquivo_csv, delimiter=';')
                print("\nHistórico de Transações:")
                for linha in leitor:
                    print(f"{linha['Data']} - {linha['Descrição']}: R$ {float(linha['Valor']):.2f}")
                saldo_final = self.carregar_saldo_inicial()
                print(f"\nSaldo atual: R$ {saldo_final:.2f}")
        except FileNotFoundError:
            print("Arquivo de extrato não encontrado.")
        except Exception as e:
            print(f"Erro ao ler o extrato: {e}")
        #final

    def grava_extrato(self):
        try:
            with open(self.extrato_filepath, 'a', newline='', encoding='utf-8') as arquivo_csv:
                escritor_csv = csv.writer(arquivo_csv, delimiter=';')
                if os.stat(self.extrato_filepath).st_size == 0:
                    escritor_csv.writerow(["Agência", "Conta", "Data", "Descrição", "Valor"])
                for data_hora, descricao, valor in self.historico:
                    escritor_csv.writerow([self.agencia, self.numero_conta, data_hora.strftime("%d/%m/%Y %H:%M:%S"), descricao, valor])
        except FileNotFoundError:
            print(f"Arquivo '{self.extrato_filepath}' não encontrado. Criando um novo...")
            self.grava_extrato() #tenta de novo caso ocorra o erro
        except Exception as e:
            print(f"Erro ao gravar extrato no arquivo: {e}")

    def extrato(self):
        print("\nEXTRATO:")
        print(f"Agência: {self.agencia}, Número da conta: {self.numero_conta}")
        try:
            with open(self.extrato_filepath, 'r', newline='', encoding='utf-8') as arquivo_csv:
                leitor = csv.DictReader(arquivo_csv, delimiter=';')
                print("\nHistórico de Transações:")
                for linha in leitor:
                    print(f"{linha['Data']} - {linha['Descrição']}: R$ {float(linha['Valor']):.2f}")
                # Calcula o saldo final no extrato (melhoria)
                saldo_final = self.carregar_saldo_inicial()
                print(f"\nSaldo atual: R$ {saldo_final:.2f}")
        except FileNotFoundError:
            print("Arquivo de extrato não encontrado.")
        except Exception as e:
            print(f"Erro ao ler o extrato: {e}")

class Banco:
    def __init__(self):
        self.usuarios_filepath = get_filepath("usuarios.csv")
        self.contas_filepath = get_filepath("contas.csv")
        self.usuarios = self.carregar_usuarios()
        self.contas = self.carregar_contas()

    def carregar_usuarios(self):
        # Implementação para carregar usuários de usuarios.csv
        try:
            with open(self.usuarios_filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                return list(reader)
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Erro ao carregar usuários: {e}")
            return []

    def salvar_usuarios(self):
        try:
            with open(self.usuarios_filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['CPF', 'Nome', 'Data de Nascimento', 'Endereço']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerows(self.usuarios)
        except Exception as e:
            print(f"Erro ao salvar usuários: {e}")

    def carregar_contas(self):
        # Implementação para carregar contas de contas.csv
        try:
            with open(self.contas_filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                return list(reader)
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Erro ao carregar contas: {e}")
            return []

    def salvar_contas(self):
        try:
            with open(self.contas_filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Agência', 'Número da Conta', 'CPF do Usuário']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerows(self.contas)
        except Exception as e:
            print(f"Erro ao salvar contas: {e}")

    def cadastrar_usuario(self):
        cpf = input("Digite o CPF (somente números): ")
        nome = input("Digite o nome: ")
        data_nascimento = input("Digite a data de nascimento (DD/MM/AAAA): ")
        endereco = input("Digite o endereço: ")
        self.usuarios.append(
            {
                "CPF": cpf,
                "Nome": nome,
                "Data de Nascimento": data_nascimento,
                "Endereço": endereco,
            }
        )
        self.salvar_usuarios()
        print("Usuário cadastrado com sucesso!")

    def cadastrar_conta(self):
        while True:
            cpf = input("Digite o CPF do usuário: ")
            usuario = next((u for u in self.usuarios if u['CPF'] == cpf), None)
            if usuario:
                break
            else:
                print("CPF não encontrado. Tente novamente.")
        agencia = "0001"
        numero_conta = len(self.contas) + 1
        self.contas.append(
            {
                "Agência": agencia,
                "Número da Conta": numero_conta,
                "CPF do Usuário": cpf,
            }
        )
        self.salvar_contas()
        print("Conta criada com sucesso!")
        return ContaBancaria(numero_conta, agencia, cpf)

    def consultar_conta(self, agencia, numero_conta):
        for conta in self.contas:
            if conta["Agência"] == agencia and conta["Número da Conta"] == str(numero_conta):
                return conta
        return None

def main():
    banco = Banco()

    while True:
        print("\nMENU PRINCIPAL:")
        print("1. Cadastrar Usuário")
        print("2. Cadastrar Conta")
        print("3. Consultar Conta")
        print("4. Acessar Conta")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            banco.cadastrar_usuario()
        elif opcao == "2":
            banco.cadastrar_conta()
        elif opcao == "3":
            agencia = input("Digite a agência: ")
            numero_conta = input("Digite o número da conta: ")
            conta = banco.consultar_conta(agencia, numero_conta)
            if conta:
                print(conta)
            else:
                print("Conta não encontrada.")
        elif opcao == "4":
            agencia = input("Digite a agência: ")
            numero_conta = input("Digite o número da conta: ")
            conta_dados = banco.consultar_conta(agencia, numero_conta)
            if conta_dados:
                cpf_usuario = conta_dados['CPF do Usuário']
                conta_bancaria = ContaBancaria(numero_conta, agencia, cpf_usuario) #criando conta
                # Interface da conta bancaria
                while True:
                    print("\nEscolha uma opção:")
                    print("1. Depósito")
                    print("2. Saque")
                    print("3. Extrato")
                    print("4. Voltar")

                    opcao_conta = input("Sua escolha: ")

                    if opcao_conta == '1':
                        valor = float(input("Digite o valor a depositar: "))
                        conta_bancaria.deposito(valor)
                    elif opcao_conta == '2':
                        valor = float(input("Digite o valor a sacar: "))
                        conta_bancaria.saque(valor)
                    elif opcao_conta == '3':
                        conta_bancaria.extrato()
                    elif opcao_conta == '4':
                        break
                    else:
                        print("Opção inválida. Tente novamente.")

            else:
                print("Conta não encontrada.")
        elif opcao == "5":
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()