# Mural de Achados e Perdidos

Aplicação web feita com Python, Flask e SQLite para cadastrar, consultar e resolver itens perdidos ou encontrados.

## Funcionalidades

- Cadastro de item perdido ou encontrado
- Nome do item
- Descrição
- Local
- Contato
- Listagem dos itens cadastrados
- Filtros: Todos, Perdidos e Encontrados
- Marcar item como Devolvido/Resolvido
- Reabrir um item resolvido
- Banco de dados SQLite criado automaticamente

## Como executar

### 1. Instale o Python

Recomendado: Python 3.10 ou superior.

### 2. Abra o terminal na pasta do projeto

```bash
cd mural_achados_perdidos
```

### 3. Crie um ambiente virtual (opcional, mas recomendado)

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Execute

```bash
python app.py
```

### 6. Acesse no navegador

http://127.0.0.1:5000

O arquivo `achados_perdidos.db` será criado automaticamente na primeira execução.
