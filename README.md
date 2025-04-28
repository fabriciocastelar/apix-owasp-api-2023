# OWASP API Security Top 10 2023 - Demo Project

## 📊 Sobre o Projeto

Este projeto demonstra de forma prática as **10 principais vulnerabilidades** do OWASP API Security Top 10 última edição.  
Até o presente momento (04/2025) a edição 2023 é a última disponibilizada pela [OWASP API Security](https://owasp.org/API-Security).

Cada vulnerabilidade é ilustrada com:
- Uma rota vulnerável (com falha proposital)
- A respectiva correção aplicada no mesmo endpoint

A demo foi desenvolvida para a palestra **"10 formas de invadir sua API — e como impedir todas elas"** no evento [APIX 2025](https://www.sensedia.com.br/apix).

---

## 📊 Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- Python 3.10+

---

## 🗓️ Como Rodar Localmente

### 1. Clone o repositório
```bash
git clone https://github.com/fabriciocastelar/apix-owasp-api-2023.git
cd apix-owasp-api-2023
```

### 2. Crie o ambiente virtual e ative-o
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Rode o servidor
```bash
uvicorn app.main:app --reload
```

API disponível em: [http://localhost:8000](http://localhost:8000)

---

## 🔢 Testes e Demonstrações

Cada vulnerabilidade está acessível via prefixo `/apiN`, onde `N` corresponde ao número da vulnerabilidade.  
Todas as rotas aceitam o header `X-Secure-Mode: true|false` para alternar entre comportamento vulnerável e seguro.  

### API-1 - Broken Object Level Authorization
**Descrição:** Controle inadequado de acesso a objetos individuais.

**Simulação:** Acessar dados de outro usuário sem permissão.
- Vulnerável:
  ```bash
  curl http://localhost:8000/api1/users/2 -H "X-User-ID: 1" -H "X-Secure-Mode: false"
  ```
- Seguro:
  ```bash
  curl http://localhost:8000/api1/users/2 -H "X-User-ID: 1" -H "X-Secure-Mode: true"
  ```
**Conclusão:** No modo seguro, acesso é negado se o ID não corresponder.

---

### API-2 - Broken Authentication
**Descrição:** Falhas na autenticação de usuários.

**Simulação:** Login aceitando credenciais inválidas.
- Vulnerável:
  ```bash
  curl -X POST http://localhost:8000/api2/login -H "Content-Type: application/json" -H "X-Secure-Mode: false" -d '{"username": "evil", "password": "123"}'
  ```
- Seguro:
  ```bash
  curl -X POST http://localhost:8000/api2/login -H "Content-Type: application/json" -H "X-Secure-Mode: true" -d '{"username": "alice", "password": "1234"}'
  ```
**Conclusão:** No modo seguro, apenas credenciais válidas funcionam.

---

### API-3 - Broken Object Property Level Authorization
**Descrição:** Modificação indevida de atributos sensíveis.

**Simulação:** Usuário comum altera campo `is_admin`.
- Vulnerável:
  ```bash
  curl -X PUT http://localhost:8000/api3/users/2 -H "Content-Type: application/json" -H "X-User-ID: 2" -H "X-Secure-Mode: false" -d '{"name": "Bob Hacker", "email": "bob@evil.com", "is_admin": true}'
  ```
- Seguro:
  ```bash
  curl -X PUT http://localhost:8000/api3/users/2 -H "Content-Type: application/json" -H "X-User-ID: 2" -H "X-Secure-Mode: true" -d '{"name": "Bob Hacker", "email": "bob@evil.com", "is_admin": true}'
  ```
**Conclusão:** Campo `is_admin` é ignorado no modo seguro.

---

### API-4 - Unrestricted Resource Consumption
**Descrição:** Consumo excessivo de recursos.

**Simulação:** Solicitação de milhares de registros sem limite.
- Vulnerável:
  ```bash
  curl "http://localhost:8000/api4/items?limit=10000" -H "X-Secure-Mode: false"
  ```
- Seguro:
  ```bash
  curl "http://localhost:8000/api4/items?limit=10000" -H "X-Secure-Mode: true"
  ```
**Conclusão:** No modo seguro, é imposto limite de 100 registros.

---

### API-5 - Broken Function Level Authorization
**Descrição:** Controle inadequado de autorização em funções administrativas.

**Simulação:** Usuário comum tenta executar uma função restrita (excluir outro usuário).
- Vulnerável:
  ```bash
  curl -X DELETE http://localhost:8000/api5/admin/delete-user/3 -H "X-User-ID: 2" -H "X-Secure-Mode: false"
  ```
- Seguro:
  ```bash
  curl -X DELETE http://localhost:8000/api5/admin/delete-user/3 -H "X-User-ID: 2" -H "X-Secure-Mode: true"
  ```
**Conclusão:** No modo seguro, apenas usuários com perfil de admin podem executar ações administrativas.

---

### API-6 - Unrestricted Access to Sensitive Business Flows
**Descrição:** Ausência de controle de acesso em fluxos de negócio críticos.

**Simulação:** Finalizar pedidos de outros usuários.
- Vulnerável:
  ```bash
  curl -X POST http://localhost:8000/api6/orders/1002/complete -H "X-Secure-Mode: false"
  ```
- Seguro:
  ```bash
  curl -X POST http://localhost:8000/api6/orders/1002/complete -H "X-User-ID: 2" -H "X-Secure-Mode: true"
  ```
**Conclusão:** No modo seguro, apenas o proprietário do pedido consegue completar a operação.

---

### API-7 - Server Side Request Forgery (SSRF)
**Descrição:** Requisições feitas pelo servidor sem validação podem expor recursos internos.

**Pré-requisito:**  Para executar esta DEMO, tem que subir um servidor na porta 80  
1º) Entrar no DOS (cmd);  
2º) Execute o comando abaixo:
  ```bash
  C:\> python -m http.server 80
  ```
3º) Executar o cURL de ataque;  
4º) Mostrar no DOS que o request chegou e não deveria.


**Simulação:** Servidor acessando `localhost` por requisição externa.
- Vulnerável:
  ```bash
  curl "http://localhost:8000/api7/fetch-url?target_url=http://127.0.0.1:80" -H "X-Secure-Mode: false"
  ```
- Seguro:
  ```bash
  curl "http://localhost:8000/api7/fetch-url?target_url=http://127.0.0.1:80" -H "X-Secure-Mode: true"
  ```
**Conclusão:** No modo seguro, URLs internas são bloqueadas.

---

### API-8 - Security Misconfiguration
**Descrição:** Configurações inseguras como debug ativo e ausência de headers de segurança.

**Simulação:** Expor informações sensíveis no debug.
- Vulnerável:
  ```bash
  curl http://localhost:8000/api8/debug -H "X-Secure-Mode: false"
  ```
- Seguro:
  ```bash
  curl -i http://localhost:8000/api8/debug -H "X-Secure-Mode: true"
  ```
**Conclusão:** No modo seguro, oculta detalhes técnicos e aplica headers de segurança.

---

### API-9 - Improper Inventory Management
**Descrição:** Endpoints internos ou antigos não documentados permanecem acessíveis.

**Simulação:** Acesso a endpoints internos e legados.
- Vulnerável:
  ```bash
  curl http://localhost:8000/api9/internal/config -H "X-Secure-Mode: false"
  ```
  ```bash
  curl http://localhost:8000/api9/v1/legacy-endpoint -H "X-Secure-Mode: false"
  ```
- Seguro:
  ```bash
  curl http://localhost:8000/api9/internal/config -H "X-Secure-Mode: true"
  ```
  ```bash
  curl http://localhost:8000/api9/v1/legacy-endpoint -H "X-Secure-Mode: true"
  ```
**Conclusão:** No modo seguro, rotas internas são escondidas ou desativadas.

---

### API-10 - Unsafe Consumption of APIs
**Descrição:** Confiar cegamente em APIs de terceiros sem validação.

**Pré-requisito:**  Para executar esta DEMO, é necessário:  
1º) Se cadastrar no site: https://www.weatherapi.com;  
2º) [Logar](https://www.weatherapi.com/login.aspx) no site;  
3º) Pegar a existente ou gerar uma nova "API Key".  

**Simulação:** Consumir resposta externa sem validar estrutura.
- Vulnerável:
  ```bash
  curl "http://localhost:8000/api10/external/weather?city=Sao Paulo&api_key=SUA_API_KEY" -H "X-Secure-Mode: false"
  ```
- Seguro:
  ```bash
  curl "http://localhost:8000/api10/external/weather?city=Sao Paulo&api_key=SUA_API_KEY" -H "X-Secure-Mode: true"
  ```
**Conclusão:** No modo seguro, apenas campos esperados são aceitos.  

---

😉 Na pasta "tests", contem o arquivo da collection Postman com todos os cenários descritos acima. É só baixar e rodar no [Postman](https://postman.com/).  ✔️  

---

## 🚀 Autor

Desenvolvido por **Fabrício Alves** para a palestra **APIX 2025** ([link do evento](https://www.sensedia.com.br/apix)).

Conecte-se comigo no [LinkedIn](https://www.linkedin.com/in/fabriciocastelar/)!

---

# Let's hack — and fix — APIs the right way! 🛡️🚀