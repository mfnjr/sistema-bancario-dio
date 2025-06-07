from datetime import datetime, date

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar(self, descricao):
        data = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.transacoes.append(f'{data} - {descricao}')

    def mostrar(self):
        print("\n--- HISTÓRICO DE TRANSAÇÕES ---")
        if not self.transacoes:
            print("Nenhuma transação realizada.")
        else:
            for linha in self.transacoes:
                print(linha)


class Conta:
    proximo_numero_conta = 1

    def __init__(self, cliente, numero):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def agencia(self):
        return self._agencia

    @property
    def numero(self):
        return self._numero

    @property
    def saldo(self):
        return self._saldo

    @classmethod
    def nova_conta(cls, cliente):
        tipo = input('Qual tipo de conta deseja criar? [1] Corrente, [2] Poupança: ').strip()
        numero = cls.proximo_numero_conta
        cls.proximo_numero_conta += 1
        if tipo == '1':
            return ContaCorrente(cliente, numero)
        elif tipo == '2':
            print("Conta poupança ainda não implementada.")
            pass
        print("Tipo inválido, criando conta corrente por padrão.")
        return ContaCorrente(cliente, numero)

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            self._historico.adicionar(f'Depósito de R$ {valor:.2f}')
            print(f'Depósito de R$ {valor:.2f} realizado. Saldo atual: R$ {self._saldo:.2f}')
        else:
            print('Valor inválido para depósito.')

    def sacar(self, valor):
        if valor <= 0:
            print('Valor inválido para saque.')
        elif valor > self._saldo:
            print(f'Saque não autorizado. Saldo insuficiente: R$ {self._saldo:.2f}')
        else:
            self._saldo -= valor
            self._historico.adicionar(f'Saque de R$ {valor:.2f}')
            print(f'Saque de R$ {valor:.2f} realizado. Saldo atual: R$ {self._saldo:.2f}')

    def saldo_e_historico(self):
        self._historico.mostrar()
        print('---')
        print(f'SALDO DE R$ {self._saldo:.2f}')


class ContaCorrente(Conta):
    LIMITE_SAQUES = 3
    LIMITE_VALOR = 500.00

    def __init__(self, cliente, numero):
        super().__init__(cliente, numero)
        self._saques_realizados = 0
        self._data_ultimo_saque = date.today()

    def sacar(self, valor):
        hoje = date.today()
        if hoje != self._data_ultimo_saque:
            self._saques_realizados = 0
            self._data_ultimo_saque = hoje

        if self._saques_realizados >= self.LIMITE_SAQUES:
            print("Limite diário de saques atingido.")
        elif valor > self.LIMITE_VALOR:
            print(f"Saque excede o limite de R$ {self.LIMITE_VALOR:.2f} por operação.")
        else:
            super().sacar(valor)
            if valor <= self.saldo + valor:  # valor foi sacado com sucesso
                self._saques_realizados += 1


class Cliente:
    _todos = {}  # cpf -> PessoaFisica

    @classmethod
    def cadastrar(cls, cliente):
        cls._todos[cliente.cpf] = cliente

    @classmethod
    def buscar_por_cpf(cls, cpf):
        return cls._todos.get(cpf)


class PessoaFisica(Cliente):
    def __init__(self):
        self._cpf = input('Digite o CPF do cliente: ').strip()
        if Cliente.buscar_por_cpf(self._cpf):
            print('CPF já cadastrado. Operação cancelada.')
            return
        self._nome = input('Digite o nome do cliente: ').strip()
        self._endereco = input('Digite o endereço: ').strip()
        self._data_nascimento = input('Digite a data de nascimento: ').strip()
        self._contas = []
        Cliente.cadastrar(self)
        agencia, numero = self.adicionar_conta()
        print(f'Cliente {self._nome} cadastrado. Agência {agencia}, Conta {numero}.')

    @property
    def cpf(self):
        return self._cpf

    def adicionar_conta(self):
        conta = Conta.nova_conta(self)
        self._contas.append(conta)
        return conta.agencia, conta.numero

    def realizar_transacao(self):
        if not self._contas:
            print('Cliente não possui contas.')
            return
        conta = self._contas[0]
        Transacao.registrar(conta)

    def ver_historico_e_saldo(self):
        if not self._contas:
            print("Cliente não possui contas.")
            return
        print("Contas disponíveis:")
        for idx, conta in enumerate(self._contas, 1):
            print(f"{idx}: Agência {conta.agencia}, Conta {conta.numero}")
        escolha = int(input("Escolha a conta para extrato: ")) - 1
        if 0 <= escolha < len(self._contas):
            self._contas[escolha].saldo_e_historico()
        else:
            print("Escolha inválida.")


class Transacao:
    @staticmethod
    def registrar(conta):
        tipo = input('Indique a operação: [D]epósito; [S]aque ').strip().upper()
        if tipo == 'D':
            Deposito().executar(conta)
        elif tipo == 'S':
            Saque().executar(conta)
        else:
            print('Transação inválida.')


class Deposito:
    def executar(self, conta):
        try:
            valor = float(input('Informe o valor para depósito: '))
            conta.depositar(valor)
        except ValueError:
            print('Valor inválido.')


class Saque:
    def executar(self, conta):
        try:
            valor = float(input('Informe o valor para saque: '))
            conta.sacar(valor)
        except ValueError:
            print('Valor inválido.')


def menu():
    clientes = []
    print('Bem-vindo ao sistema bancário 3.0!')
    while True:
        print('\n[N] Cadastrar novo cliente')
        print('[C] Cadastrar nova conta')
        print('[D] Depositar')
        print('[S] Sacar')
        print('[E] Emitir extrato')
        print('[Q] Sair')
        opc = input('Opção: ').strip().upper()
        if opc == 'N':
            cliente = PessoaFisica()
            if hasattr(cliente, '_cpf') and cliente.cpf not in Cliente._todos:
                clientes.append(cliente)
        elif opc in ('C','D','S','E'):
            cpf = input('Digite o CPF do cliente: ').strip()
            cliente = Cliente.buscar_por_cpf(cpf)
            if not cliente:
                print('Cliente não encontrado. Cadastre primeiro.')
                continue
            if opc == 'C':
                agencia, numero = cliente.adicionar_conta()
                print(f'Conta criada: Agência {agencia}, Conta {numero}')
            elif opc == 'D' or opc == 'S':
                cliente.realizar_transacao()
            elif opc == 'E':
                cliente.ver_historico_e_saldo()
        elif opc == 'Q':
            print('Saindo...')
            break
        else:
            print('Opção inválida.')


if __name__ == '__main__':
    menu()
