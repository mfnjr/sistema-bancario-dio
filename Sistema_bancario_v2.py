# DESAFIO

# Criar um sistema bancário com as operações sacar, depositar e visualizar extrato (v1).
# Separar funções existentes de saque, depósito e extrato em funções e criar funções para cadastrar usuário (cliente) e cadastrar conta (v2).

import os

LIMITE_SAQUE = 500
AGENCIA = '0001'

lista_de_depositos = []
lista_de_saques = []
lista_de_usuarios = []
lista_de_contas = []

saques_permitidos = 3
saldo = 0
numero_da_conta = 0

def cadastrar_usuario(lista_de_usuarios):

    # O programa deve armazenar os usuários em uma lista;
    # Cada usuário é composto por nome, data de nascimento, CPF e endereço;
    # O endereço é uma string com formato logradouro - bairro - cidade/UF;
    # Deve ser armazenado somente os números do CPF;
    # Não podem ser cadastrados 2 usuários com o mesmo CPF.

    cpf_do_usuario = input('Digite o CPF do cliente: ').replace('.','').replace('-','')

    if len(lista_de_usuarios) > 0:

        for i in lista_de_usuarios:

            if i[3] == cpf_do_usuario:

                print('\nJá existe um cadastro para este CPF. Operação cancelada!')
                
                return None, None
    
    nome_do_usuario = input('Digite o nome do cliente: ')
    data_de_nascimento = input('Digite a data de nascimento no formato dd/mm/aaaa: ')
    logradouro = input('Digite o logradoudo do cliente: ')
    bairro = input('Digite o bairro do cliente: ')
    cidade = input('Digite a cidade do cliente: ')
    uf = input('Digite a UF do cliente: ')

    novo_cliente = [nome_do_usuario, data_de_nascimento, f'{logradouro} - {bairro} - {cidade}/{uf}', cpf_do_usuario]

    return novo_cliente, cpf_do_usuario

def cadastrar_conta(cpf_do_usuario, lista_de_usuarios):

    # O programa deve armazenar contas em uma lista.
    # Uma conta é composta por agência, número da conta e usuário.
    # O número da conta é sequencial, iniciando em 1
    # O número da agência é fixo: 0001
    # O usuário pode ter mais de uma conta, mas uma conta pode pertencer só a 1 usuário.
    # Dica: para vincular um usuário a uma conta, filtre a lista de usuários buscando o CPF informado para cada usuário.

    global numero_da_conta

    for i in lista_de_usuarios:

        if i[3] == cpf_do_usuario:

            nome_do_usuario = i[0]

    numero_da_conta += 1    
    nova_conta = [AGENCIA, numero_da_conta, nome_do_usuario]

    return nova_conta

def depositar(valor_deposito):

    # Deve ser possível depositar valores positivos para a conta. 
    # Todos os depósitos devem ser armazenados em uma variável e exibidos na operação de extrato.

    # A função de depósito deve receber os argumentos apenas por posição.

    global saldo, lista_de_depositos

    saldo += valor_deposito
    lista_de_depositos.append(valor_deposito)

    print(f'\nDepósito de R$ {valor_deposito:.2f} realizado com sucesso!')

def sacar(*, valor_sacado):

    # O sistema deve permitir realizar 3 saques diários com limite máximo de R$ 500,00 por saque. 
    # Caso o usuário não tenha saldo, o sistema deve exibir uma mensagem informando que não será possível sacar o dinheiro por falta de saldo. 
    # Todos os saques devem ser armazenados em uma variável e exibido na operação de extrato.

    # A função de saque deve receber argumentos apenas por nome (keyword only).

    global saldo, lista_de_saques, saques_permitidos
    
    saldo -= valor_sacado
    lista_de_saques.append(valor_sacado)
    saques_permitidos -= 1

    print(f'\nSaque de R$ {valor_sacado:.2f} realizado com sucesso!')

def visualizar_extrato(saldo, *, depositos_realizados, saques_realizados):

    # Na operação de extrato, o sistema deve listar todos os depósitos e saques realizados. 
    # No fim da listagem, deve ser exibido o saldo atual.
    # Os valores devem ser exibidos utilizando o formato R$ 0,00.

    # A função de extrato deve receber os argumentos por posição e nome.
    
    if len(depositos_realizados) == 0 and len(saques_realizados) == 0:

        print('\nNenhuma movimentação realizada até o momento.')
    
    else:

        print('\nExtrato:')
        print('\nDepósitos:\n')
        
        for deposito in depositos_realizados:
            print(f'- R$ {deposito:.2f}')

        print('\nSaques:\n')

        for saque in saques_realizados:
            print(f'- R$ {saque:.2f}')

        print(f'\nSaldo atual: R$ {saldo:.2f}')

os.system('cls' if os.name == 'nt' else 'clear')     
print('Bem-vindo ao sistema bancário 2.0!\n\n[N] Cadastrar novo cliente\n[C] Cadastrar nova conta\n[D] Depositar dinheiro\n[S] Sacar dinheiro\n[E] Emitir extrato\n[Q] Sair do sistema')

while True:  
    
    opcao = input('\nEscolha uma opção das opções do menu: ').strip().upper()
    
    if opcao == 'N':
        
        novo_usuario, cpf_do_usuario = cadastrar_usuario(lista_de_usuarios)

        if novo_usuario is not None:

            lista_de_usuarios.append(novo_usuario)           
            nova_conta = cadastrar_conta(cpf_do_usuario, lista_de_usuarios)

            print(f'\nO(A) cliente {nova_conta[2]} foi cadastrado(a) com sucesso para a Agência n.º {nova_conta[0]}, Conta n.º {nova_conta[1]}.')
    
    elif opcao == 'C':

        usuario_previamente_cadastrado = False
        cpf_do_usuario = input('\nDigite o CPF do cliente: ').replace('.','').replace('-','')

        for i in lista_de_usuarios:

            if i[3] == cpf_do_usuario:

                usuario_previamente_cadastrado = True
                print(f'\nCadastrando conta adicional para o(a) usuário(a) {lista_de_usuarios[0][0]}...')

                nova_conta = cadastrar_conta(cpf_do_usuario, lista_de_usuarios)

                print(f'\nO(A) cliente {nova_conta[2]} foi cadastrado(a) com sucesso para a Agência n.º {nova_conta[0]}, Conta n.º {nova_conta[1]}.')

        if not usuario_previamente_cadastrado:

            print('\nNão há usuário cadastrado para o CPF informado. Proceda, antes, ao cadastro do usuário.')
    
    elif opcao == 'D':
        
        valor_deposito = float(input('\nDigite o valor que deseja depositar: R$ '))
        
        if valor_deposito <= 0:

            print('\nValor inválido! O depósito deve ser maior que R$ 0,00.')
            continue

        depositar(valor_deposito)
    
    elif opcao == 'S':
        
        if saques_permitidos <= 0:

            print('\nNúmero máximo de saques diários atingido! Operação não permitida.')
            continue
        
        valor_saque = float(input('\nDigite o valor que deseja sacar: R$ '))

        if valor_saque > LIMITE_SAQUE:

            print(f'\nOperação não permitida. O valor máximo para saque disponível para você é de R$ {LIMITE_SAQUE:.2f}.')
            continue
        
        else:

            if valor_saque <= 0:
                
                print('\nValor inválido! O saque deve ser maior que R$ 0,00.')
                continue
            
            if valor_saque > saldo:

                print(f'\nO saldo atual de {saldo:.2f} é insuficiente para realizar o saque.')
                continue

        sacar(valor_sacado=valor_saque)

    elif opcao == 'E':

        visualizar_extrato(saldo, depositos_realizados=lista_de_depositos, saques_realizados=lista_de_saques)
            
    elif opcao == 'Q':
        
        print('\nObrigado por utilizar o nosso sistema! Volte sempre!\n')
        break

    else:

        print('\nOpção inválida! Tente novamente.')