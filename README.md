# Processo Seletivo LuizaLabs - 10/2019

Este serviço é responsável por armazenar quais são os produtos favoritos de um determinado cliente.

Todas as rotas são protegidas por um token JWT, este que deve ser obtido na rota de login.

**Índice**
1. [Requisitos](#cs0)
2. [Informações adicionais](#cs1)
3. [Configuração do ambiente](#cs2)
4. [Comandos úteis](#cs3)
5. [Tecnologias utilizadas](#cs4)
6. [Imagens](#cs5)

## Requisitos <a name="cs0"></a>
- Python 3.x
- Postgres
- Redis

## Informações adicionais <a name="cs1"></a>
O arquivo `.env.example` serve para setar variáveis de ambiente em modo de desenvolvimento ou teste.
Para que haja efeito deve-se renomear o arquivo para `.env`.

O banco de dados padrão para armazenamento dos dados é o `postgres`.

Após fazer a configuração inicial, pode-se acessar as rotas do projeto pela URL `http://localhost:5000/docs`

Na documentação há uma rota `/auth/register` que deve ser usada para fazer o primeiro cadastro no sistema.

Após fazer o cadastro, deve-se utilizar a rota `/auth/login` para obter o token de acesso às demais rotas, este que deve ser injetado no header `authorization`.

Será gerado dois tokens (access_token e refresh_token). Para acessar as rotas é recomendado utilizar somente o `access_token` e caso o mesmo expire, pode-se utilizar o `refresh_token` para obter um novo token. Todos os dois tokens tem uma vida útil de 15 e 30 minutos respectivamente.

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

## Comandos úteis <a name="cs3"></a>
Rodar o lint para organização do código
````bash
flask db commands lint
````

Rodar o teste de complexidade do código
````bash
flask db commands complexity
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

## Técnologias utilizadas <a name="cs4"></a>
- Python: linguagem de programação utilizada no desenvolvimento do serviço;
- Postgres: banco de dados relacional utilizado para armazenar os dados;
- Git: tecnologia para controle de versão do código;
- Flask: micro-framework para gerenciamento web;
- SQLAlchemy: biblioteca de objeto-relacional para manipulação de SQL;
- Marshmallow: biblioteca para validação de dados de entrada e saída;
- Restplus: biblioteca para criação da documentação das rotas da aplicação;
- Requests: biblioteca para realização de chamadas em outros sites/api's;
- Radon: biblioteca para verificar a complexidade dos códigos;
- Pre-commit: biblioteca que define os padrões do PEP 8, quando é feito um commit;

## Imagens <a name="cs5"></a>
![Alt text](/doc.png "Documentação da aplicação")
