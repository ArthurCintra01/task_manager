# Projeto Task Manager

Este programa apresenta um sistema de cadastro de projetos com datas de início e fim e um número ilimitado de atividades para cada projeto.

## Tecnologias usadas

* Python 3.7.0

* SQLAlchemy 1.4.18 (Biblioteca usada para implementação das tabelas em um banco de dados SQLITE)

* prettytable 2.1.0 (Biblioteca usada para implementar a interface das tabelas de projetos e atividades)

## Instalação das bibliotecas

Foram feitas através do package manager [pip](https://pip.pypa.io/en/stable/) usando:

Para a biblioteca prettytable:
```
pip install prettytable
```
Para a biblioteca SQLAlchemy:
```
pip install SQLAlchemy
```

## Programação
Criei duas tabelas na database para guardar os projetos e atividades, criei um menu simples para mostrar as opções ao usuário, assim, usando as ferramentas do SQLAlchemy fiz a manipulação das tabelas de acordo com a ação do usuário e mostrei as informações necessarias das tabelas usando a biblioteca prettytable.

## Uso do programa

O usuário pode executar o programa usando o comando:
```
desafio.py
```
Após executar o programa o usuário será apresentado a uma tabela com os projetos salvos no banco de dados e um menu com as opções que o usuário pode selecionar.

Depois da ação ser realizada o programa volta a mostrar a tabela de projetos e o menu.

Todas as ações feitas pelo usuário são salvas na database para uso futuro.

### Observações

* Se na entrada de datas, a data de inicio for maior que a de fim o programa pedirá que insira as datas novamente até estar adequado.

* Se um projeto for deletado todas as atividades daquele projeto também serão deletadas.

* Depois de um projeto ser deletado, se houver projetos com ids maiores que a dele a id do projeto não será usada novamente e as próximas ids terão valores a partir da maior id cadastrada.

# Licença
The MIT License [MIT](https://choosealicense.com/licenses/mit/)

Copyright (c) [2021] [Arthur Pereira Mazzoni Cintra]

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
