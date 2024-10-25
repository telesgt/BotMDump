# MacacoDump

MacacoDump é o projeto para gerar os dumps de personagens a serem utilizados pelo MacacoBot

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