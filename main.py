def saque(*, saldo: float, extrato: str, limite: int,
          num_saques: int, limite_saques: int) -> tuple[float, str]:
    print(' Saque '.center(50, '#'), '\n')

    while True:

        if saldo == 0:
            print('Você não tem nenhum saldo.\n')
            break

        valor_saque = float()

        if num_saques < limite_saques:
            valor_saque = float(input('Digite o valor que deseja sacar: '))

        elif num_saques >= limite_saques:
            print('Você atingiu o limite de saques diários '
                  f'atual que é de {limite_saques} saques.\n')
            break

        if valor_saque > 500:
            print('Valor do saque maior que o permitido, '
                  f'insira um valor menor que {limite}.\n')

        elif valor_saque <= 0:
            print('Valor inválido, digite um número maior que 0!\n')

        elif valor_saque > saldo:
            print('\nO valor do saque é maior que o saldo atual, '
                  f'insira um valor menor ou igual a R$ {saldo:.2f}\n')

        elif valor_saque > 0 and valor_saque <= saldo:
            saldo -= valor_saque
            num_saques += 1
            extrato += f'Saque: || R$ {valor_saque:.2f}' + ' | '
            print('\nSaque realizado com sucesso.\n'
                  f'Saldo atual é de R$ {saldo:.2f}\n')
            break

    return saldo, extrato


def deposito(saldo: float, extrato: str, /) -> tuple[float, str]:
    print(' Depósito '.center(50, '#'), '\n')

    valor_deposito = float()

    while True:
        valor_deposito = float(input('Digite o valor que deseja depositar: '))

        if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f'Depósito: || R$ {valor_deposito:.2f}' + ' | '
            print('\nDepósito realizado com sucesso.\n'
                  f'Saldo atual: R$ {saldo:.2f}.\n')
            break

        else:
            print('O valor não é válido, digite um número maior que 0!\n')

    return saldo, extrato


def mostrar_extrato(saldo: float, /, *, extrato: str) -> None:
    print(' Extrato '.center(50, '#'), '\n')

    if extrato:
        lista_saques = extrato.rstrip(' | ').split(' | ')

        print('\nAqui estão todas as suas operações:\n')

        for operacao in lista_saques:
            tipo, valor = operacao.split(' || ')
            print(tipo.center(15), valor)

        print(f'\nSaldo atual: R$ {saldo:.2f}\n')

    else:
        print('Não foram realizadas movimentações.\n')


def filtrar_usuario(cpf: str,
                    usuarios: list[dict[str, str]]
                    ) -> dict[str, str] | None:
    usuario = [user for user in usuarios if user.get('cpf') == cpf]
    return usuario[0] if usuario else None


def filtrar_digitos_cpf(cpf: str) -> str:
    return ''.join(digit for digit in cpf if digit.isdigit())


def cadastrar_usuario(usuarios):
    print('\n', ' Criar Usuário '.center(50, '#'), '\n')
    cpf_in = input('Digite o CPF do usuário: ')
    cpf = filtrar_digitos_cpf(cpf_in)

    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print('Erro na Operação. Usuário já cadastrado com o cpf informado!')
        return

    else:
        nome = input('Nome Completo: ')
        data_nascimento = input('Data de nascimento (dd-mm-AAAA): ')
        endereco = input('Digite o endereço '
                         '(logradouro, nro - bairro - cidade/sigla estado): ')

        usuario = {'nome': nome, 'data_nascimento': data_nascimento,
                   'cpf': cpf, 'endereco': endereco}
        usuarios.append(usuario)
        print('\nUsuário cadastrado com sucesso.')
    print('\n')


def criar_conta(contas: list[dict[str, str | int | dict]],
                usuarios: list[dict[str, str]]):
    print('\n', ' Criar Conta '.center(50, '#'), '\n')
    cpf_usuario = input('Digite o cpf do usuário: ')

    cpf_usuario = filtrar_digitos_cpf(cpf_usuario)
    usuario = filtrar_usuario(cpf_usuario, usuarios)

    if not usuario:
        print('\nErro na operação! '
              'Nenhum usuário encontrado para o cpf informado.\n')
        return

    num_conta = len(contas) + 1
    conta = {'agencia': '0001', 'num_conta': num_conta, 'usuario': usuario}
    contas.append(conta)
    print(f'\nConta criada com sucesso, o número da conta é {num_conta}\n')


def listar_contas(contas: list[dict]):
    print('\n', ' Lista de Contas '.center(50, '#'), '\n')

    for conta in contas:
        print(
            f'Agência:..........{conta["agencia"]}',
            f'Número da conta:..{conta["num_conta"]}',
            f'Usuário:..........{conta["usuario"]["nome"]}',
            sep='\n',
            end='\n\n'
        )


def main():
    menu = '''
[d] Depositar
[s] Sacar
[e] Extrato
[1] Novo Usuário
[2] Nova Conta
[3] Listar Todas as Contas
[q] Sair

=> '''

    usuarios: list[dict[str, str]] = list()
    contas: list[dict[str, str | int | dict[str, str]]] = list()
    saldo = float()
    extrato = str()
    num_saques = 0
    limite_por_saque = 500
    limite_qtde_saques = 3

    while True:
        print(' Menu '.center(50, '#'))
        opcao = input(menu)

        if opcao == 'd':
            saldo, extrato = deposito(saldo, extrato)

        elif opcao == 's':
            saldo, extrato = saque(
                saldo=saldo,
                extrato=extrato,
                limite=limite_por_saque,
                num_saques=num_saques,
                limite_saques=limite_qtde_saques
            )

        elif opcao == 'e':
            mostrar_extrato(saldo, extrato=extrato)

        elif opcao == 'q':
            print('Sair...')
            break

        elif opcao == '1':
            cadastrar_usuario(usuarios)

        elif opcao == '2':
            criar_conta(contas, usuarios)

        elif opcao == '3':
            listar_contas(contas)

        else:
            print('Operação inválidam por favor selecione '
                  'novamente a operação desejada.')


main()
