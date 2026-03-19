# API de Assistente Virtual com IA para Academias

## Visão Geral
Este projeto implementa um backend robusto para um assistente virtual de WhatsApp focado na retenção, atendimento e engajamento de alunos de academias. Desenvolvido em Python, o sistema integra a API Oficial do WhatsApp (Meta) com o modelo de linguagem Gemini 1.5 Pro do Google, utilizando LangChain para orquestração de contexto.

O diferencial arquitetônico deste sistema é a capacidade de injetar o contexto real do aluno (buscado via banco de dados relacional) diretamente no prompt da IA. Isso permite que o LLM tome decisões e gere respostas altamente personalizadas baseadas no objetivo de treino do aluno, seu nível de experiência e o status financeiro de sua mensalidade.

## Tecnologias e Arquitetura
A stack foi rigorosamente selecionada com foco em performance assíncrona, manutenibilidade e integração fluida com ferramentas modernas de Inteligência Artificial:

* [cite_start]**Backend:** FastAPI e Uvicorn para roteamento e processamento assíncrono de webhooks.
* [cite_start]**Orquestração de IA:** LangChain Core e LangChain Google GenAI (Gemini 1.5 Pro) para formatação de prompts dinâmicos e geração de texto.
* [cite_start]**Banco de Dados:** SQLite (focado em desenvolvimento ágil) manipulado via ORM SQLAlchemy.
* [cite_start]**Integrações Externas:** HTTPX para requisições assíncronas direcionadas à Meta Graph API.
* [cite_start]**Segurança:** Python-dotenv para isolamento estrito de credenciais de ambiente.

## Funcionalidades Principais
1. **Recebimento e Processamento Assíncrono:** Webhooks configurados para receber payloads da Meta, extraindo e validando de forma segura o número do remetente e o corpo da mensagem.
2. **Autenticação de Webhook Externa:** Implementação de rota de verificação de segurança (método GET) com validação de token, atendendo aos requisitos obrigatórios da documentação oficial da Meta.
3. **Orquestração de Contexto (Abordagem RAG Simplificada):** Antes de acionar o LLM, o sistema consulta o cadastro do aluno. A IA recebe instruções de sistema ("System Prompt") variáveis, adaptando o tom e o conteúdo da resposta com base em lógicas de negócio predefinidas.
4. **Resiliência e Tratamento de Erros:** Blocos `try/except` abrangentes garantem que falhas de rede com a API do Google ou dados malformados recebidos da Meta não causem quedas silenciosas na aplicação. Todas as ocorrências são registradas via logs estruturados de sistema.

## Estrutura do Projeto
* `main.py`: Ponto de entrada da aplicação, contendo a definição de rotas FastAPI, lógica de extração de webhooks e tratamento de exceções.
* `ai_agent.py`: Configuração da chain do LangChain, definição dos templates de prompt e integração direta com o Google Gemini.
* `database.py`: Configuração do motor do banco de dados e gerenciamento de sessões seguras do SQLAlchemy.
* `models.py`: Mapeamento objeto-relacional (ORM), definindo a tabela de alunos e regras de restrição de dados utilizando Enums do Python.
* `whatsapp_utils.py`: Módulo utilitário isolado para montagem de headers, payloads e envio de requisições HTTP POST para a API do WhatsApp.
* [cite_start]`requirements.txt`: Documentação da árvore de dependências do ambiente.

## Como Executar Localmente

### 1. Pré-requisitos
Certifique-se de possuir o Python 3.10 ou superior instalado em sua máquina.

### 2. Clonar e Configurar o Ambiente
Clone este repositório e crie um ambiente virtual para isolar as dependências:
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA>
python -m venv venv
```

# Ativação no Windows:
venv\Scripts\activate
# Ativação no Linux/Mac:
source venv/bin/activate

### 3. Instalar Dependências
Instale as bibliotecas requeridas pelo projeto:
```bash
pip install -r requirements.txt
```

### 4. Configuração de Variáveis de Ambiente
Crie um arquivo chamado .env na raiz do projeto. Este arquivo deve conter as suas credenciais de acesso às APIs externas:

GOOGLE_API_KEY=sua_chave_do_gemini_aqui
WHATSAPP_TOKEN=seu_token_de_acesso_da_meta
WHATSAPP_PHONE_NUMBER_ID=seu_id_de_telefone_aqui
WEBHOOK_VERIFY_TOKEN=senha_secreta_academia_123

### 5. Inicie a aplicação utilizando o Uvicorn para habilitar o recarregamento automático (hot-reload):

```bash
uvicorn main:app --reload
```

O servidor estará ativo em http://127.0.0.1:8000. O banco de dados relacional (academia.db) e as respectivas tabelas serão criados automaticamente pelo SQLAlchemy durante a primeira execução.

