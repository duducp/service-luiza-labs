# Processo Seletivo LuizaLabs - 10/2019

Este serviço é responsável por armazenar quais são os produtos favoritos de um determinado cliente.

Todas as rotas são protegidas por um token JWT, este que deve ser obtido na rota de login.

**Índice**
1. [Requisitos](#cs0)
2. [Informações adicionais](#cs1)
3. [Configuração do ambiente](#cs2)
4. [Comandos úteis](#cs3)

## Requisitos <a name="cs0"></a>
- Python 3.x
- Postgres
- Redis

## Informações adicionais <a name="cs1"></a>
O arquivo `.env.example` serve para setar variáveis de ambiente em modo de desenvolvimento ou teste.
Para que haja efeito deve-se renomear o arquivo para `.env`.

O banco de dados padrão para armazenamento dos dados é o `postgres`.

Todo o projeto segue um padrão pré definido pelo pre-commit.

## Configuração do ambiente <a name="cs2"></a>
Iniciar ambiente virtual
````bash
python -m venv venv
````

Ativar ambiente virtual
````bash
- Linux
source venv/bin/activate

- Windows
venv\Scripts\activate
````

Instalar dependências
````bash
pip install -r requirements.txt
````

Após configurar os dados de conexão com o banco de dados, rodar o comando
````bash
flask config create-db luizalabs
````

Aplicar as migrations no banco de dados
````bash
flask db upgrade
````

Iniciar a aplicação
````bash
flask run
````

Acessar a documentação (não disponível para o modo de produção)
````bash
http://localhost:5000/docs
````

#### Comandos úteis <a name="cs3"></a>
Rodar o lint para organização do código
````bash
flask db commands lint
````

Rodar o teste de complexidade do código
````bash
flask db commands complexity
````

Rodar os cenários de testes
````bash
flask db commands test
````

Criar um database no Postgres
````bash
flask db config create-db NOME_DATABASE
````

Ver todas as rotas da aplicação
````bash
flask routes
````

Ver comandos do database
````bash
flask db
````

Rodar aplicação
````bash
flask run
````
