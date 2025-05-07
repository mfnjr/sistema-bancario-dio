# Criar um sistema bancário com as operações sacar, depositar e visualizar extrato.

import os

LIMITE_SAQUE = 500

lista_de_depositos = []
lista_de_saques = []
saques_permitidos = 3
saldo = 0

def depositar(valor_deposito):

    '''
    Deve ser possível depositar valores positivos para a conta. A v1 do projeto trabalha com apenas 1 usuário, de modo que não é preciso se preocupar em identificar qual é o número da 
    agência e a conta bancária.
    Todos os depósitos devem ser armazenados em uma variável e exibidos na operação de extrato.'''

    global saldo, lista_de_depositos

    saldo += valor_deposito
    lista_de_depositos.append(valor_deposito)

    print(f'\nDepósito de R$ {valor_deposito:.2f} realizado com sucesso!')

def sacar(valor_saque):

    '''O sistema deve permitir realizar 3 saques diários com limite máximo de R$ 500,00 por saque. Caso o usuário não tenha saldo, o sistema deve exibir uma mensagem informando que não será 
    possível sacar o dinheiro por falta de saldo. Todos os saques devem ser armazenados em uma variável e exibido na operação de extrato.'''

    global saldo, lista_de_saques, saques_permitidos
    
    saldo -= valor_saque
    lista_de_saques.append(valor_saque)
    saques_permitidos -= 1

    print(f'\nSaque de R$ {valor_saque:.2f} realizado com sucesso!')

def visualizar_extrato():

    '''Na operação de extrato, o sistema deve listar todos os depósitos e saques realizados. No fim da listagem, deve ser exibido o saldo atual.
    Os valores devem ser exibidos utilizando o formato R$ 0,00.'''

    global saldo, lista_de_depositos, lista_de_saques
    
    if len(lista_de_depositos) == 0 and len(lista_de_saques) == 0:

        print('\nNenhuma movimentação realizada até o momento.')
    
    else:

        print('\nExtrato:')
        print('\nDepósitos:\n')
        
        for deposito in lista_de_depositos:
            print(f'- R$ {deposito:.2f}')

        print('\nSaques:\n')

        for saque in lista_de_saques:
            print(f'- R$ {saque:.2f}')

        print(f'\nSaldo atual: R$ {saldo:.2f}')

os.system('cls' if os.name == 'nt' else 'clear')     
print('Bem-vindo ao sistema bancário 1.0!\n\n[D] Depositar dinheiro\n[S] Sacar dinheiro\n[E] Emitir extrato\n[Q] Sair do sistema')

while True:  
    
    opcao = input('\nEscolha uma opção das opções do menu: ').strip().upper()
    
    if opcao == 'D':
        
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

        sacar(valor_saque)

    elif opcao == 'E':

        visualizar_extrato()
            
    elif opcao == 'Q':
        
        print('\nObrigado por utilizar o nosso sistema! Volte sempre!\n')
        break

    else:

        print('\nOpção inválida! Tente novamente.')