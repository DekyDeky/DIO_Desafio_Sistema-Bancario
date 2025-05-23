# 🧪 Lab Project: Criando um Sistema Bancário 🏦
O repositório em questão foi criado para armazenar os arquivos relacionados aos desafios de Sistema Bancário da trilha de Python da Suzano em parceria com a Dio.
## Sobre o Desafio 1 🎯 (desafio.py)
O desafio propôs a criação de um sistema bancário simples de apenas uma conta que obtem de 3 funções principais: Depósito, Saque e Extrato.
### Requisitos - Depósito 🪙
- Deve se depositar apenas valores positivos;
- Todos os depósitos devem ser imprimidos no extrato.
### Requisitos - Saque 💸
- O usuário pode ter apenas 3 Saques diários;
- Todo saque tem um limite de até R$ 500,00;
- O usuário não pode sacar valores superiores ao seu saldo;
- Todos os Saques devem ser imprimidos no extrato.
### Requisitos - Extrato 🧾
- A função deve listar todos os depósitos e saques
- Também deve exibir o saldo atual da conta
- Se não houve movimentação na conta, deve-se exibir a mensagem "Não foram realizadas movimentações."


## Sobre o Desafio 2 🎯 (desafio2.py)
O desafio 2 se trata de uma atualização do sistema bancário, onde é necessário a atualização das funções criadas anteriomente e a adição de 2 novas funções.
### Requisitos - Atualização das funções: Depósito, Saque e Extrato 🔝
- Agora a função Depósito deve receber parâmetros do tipo *positional only*
- A função Sacar deve ter como parâmetros apenas entradas do tipo *keyword only*
- E a função Extrato pode ter tanto *positional only* quanto *keyword only* como parâmetro.
### Requisitos - Função de criar usuário 👤
- A nova função deve criar um novo usuário e adicioná-lo em uma lista.
- O usuário deve conter Nome, Data de Nascimento, CPF e Endereço
- O endereço deve ser formatado da seguinte forma: "Logradouro, Bairro, Cidade/Sigra Estado".
- Não pode haver dois usuários com o mesmo CPF.
### Requisitos - Função de criar conta corrente 📩
- A função deve vincular um usuário a uma conta corrente.
- Um usuário pode ter multíplas contas correntes, mas uma conta corrente pode ter apenas 1 usuário.
- O número da conta deve ser sequencial, iniciando em 1.
- A conta deve conter o número da agência "0001", sendo ele um valor fixo.