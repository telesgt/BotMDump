# MacacoDump

Um projeto para gerar os dumps de personagens a serem utilizados pelo Bot

## Como executar

### Baixando dependências

Para o gerenciamento de dependências do projeto, utilizamos o pipenv. Portanto, será necessário instalar ele pelo pip.

```
pip install --user pipenv
```

(Opcional) Depois de instalar, caso queira manter as dependências dentro de uma pasta .venv no projeto, configure a seguinte variável de ambiente.
```
PIPENV_VENV_IN_PROJECT=true
```

Com o pipenv instalado, podemos baixar as dependências do projeto.

```
pipenv install
```

### Configurando docker

Via prompt, abrir a pasta docker e executar o comando

```
docker-compose up
```
OU
```
docker-compose up -d
```

A interface web estará disponível através da url localhost:8081

### Variáveis de Ambiente

Crie na raiz um arquivo .env com a seguinte propriedade

```
DB_URI="mongodb://root:example@127.0.0.1"
```

### Executando o projeto

O projeto é executado a partir do main.py, porém como estamos usando o pipenv, executamos ele da seguinte forma.

```
pipenv shell
py main.py
```
OU
```
pipenv run py main.py
```
