![Company:](https://cdn.prod.website-files.com/64ac7bf2029f08bfbbe5c7d2/64ac7bf2029f08bfbbe5c90e_Sensedia_horizontal_color-01.svg)
![APIX:](https://cdn.prod.website-files.com/6474ba281ebb6ae9242441af/6489a225c51875fda6922b9c_Apix%20logo.svg)  
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

# OWASP API Security Top 10 2023 - Demo Project

## 📊 Sobre o Projeto

**Este projeto demonstra de forma LÚDICA as 10 principais vulnerabilidades** do OWASP API Security Top 10 última edição.  
Até o presente momento (04/2025) a edição 2023 é a última disponibilizada pela [OWASP API Security](https://owasp.org/API-Security).

Cada vulnerabilidade é ilustrada com:
- Uma rota vulnerável 🔓 (com falha simples e proposital)
- A respectiva correção 🔐 aplicada no mesmo endpoint (também de forma simples)

A DEMO foi desenvolvida para a palestra **"10 formas de invadir sua API - e como impedir todas elas"** no evento [APIX 2025](https://www.sensedia.com.br/apix).

## 📢 Sobre a Demo
A gente bem que queria mostrar APIs reais e cheias de falhas - e olha que não faltam candidatas no mundo real.  
Mas, por uma questão de “boa vizinhança” com os devs por aí (e para evitar processos desnecessários), resolvemos pegar leve.
Em vez disso, montamos um ambiente local, **100% vulnerável e 1000% intencional**.  
Aqui, as falhas de segurança são por design - porque às vezes, para aprender a proteger, é preciso primeiro aprender a invadir... **sem ir preso no processo.** 😎

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
*Falhas no controle de acesso a objetos.*  
**Descrição:** Controle inadequado de acesso a objetos individuais.

**Simulação:** Acessar dados de outro usuário sem permissão.
- 🔓 Vulnerável:
  ```bash
  curl http://localhost:8000/api1/users/2 -H "X-User-ID: 1" -H "X-Secure-Mode: false"
  ```
- 🔐 Seguro:
  ```bash
  curl http://localhost:8000/api1/users/2 -H "X-User-ID: 1" -H "X-Secure-Mode: true"
  ```
**Conclusão:** No modo seguro, acesso é negado se o ID não corresponder.  

**Recomendação Final:**  
Embora o exemplo seja simples, essa falha é extremamente comum em APIs. Reforce sua estratégia de controle de acesso com validações de autorização por objeto em todos os endpoints e implemente uma governança centralizada para regras de acesso a dados sensíveis. Este requisito é mais de negócio (funcional) do que técnico (não funcional).  
[+informações referente a vulnerabilidade API-1.](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization)

---

### API-2 - Broken Authentication
*Autenticação falha ou ausente.*  
**Descrição:** Falhas na autenticação de usuários.

**Simulação:** Login aceitando credenciais inválidas.
- 🔓 Vulnerável:
  ```bash
  curl -X POST http://localhost:8000/api2/login -H "Content-Type: application/json" -H "X-Secure-Mode: false" -d '{"username": "evil", "password": "123"}'
  ```
- 🔐 Seguro:
  ```bash
  curl -X POST http://localhost:8000/api2/login -H "Content-Type: application/json" -H "X-Secure-Mode: true" -d '{"username": "alice", "password": "1234"}'
  ```
**Conclusão:** No modo seguro, apenas credenciais válidas funcionam.  

**Recomendação Final:**  
Evite implementar autenticação manual diretamente na API. Utilize sempre soluções consolidadas, como API Gateways com Authorization Server (ex: OAuth2, OpenID Connect). Se for necessário acessar dados diretamente, prefira ORMs seguros e maduros como Hibernate, Entity Framework, Django ou Sequelize, que ajudam a evitar erros comuns de segurança e autenticação.  
[+informações referente a vulnerabilidade API-2.](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication)

---

### API-3 - Broken Object Property Level Authorization
*Falta de validação em propriedades do objeto.*  
**Descrição:** Modificação indevida de atributos sensíveis.

**Simulação:** Usuário comum altera campo `is_admin`.
- 🔓 Vulnerável:
  ```bash
  curl -X PUT http://localhost:8000/api3/users/2 -H "Content-Type: application/json" -H "X-User-ID: 2" -H "X-Secure-Mode: false" -d '{"name": "Bob Hacker", "email": "bob@evil.com", "is_admin": true}'
  ```
- 🔐 Seguro:
  ```bash
  curl -X PUT http://localhost:8000/api3/users/2 -H "Content-Type: application/json" -H "X-User-ID: 2" -H "X-Secure-Mode: true" -d '{"name": "Bob Hacker", "email": "bob@evil.com", "is_admin": true}'
  ```
**Conclusão:** Campo `is_admin` é ignorado no modo seguro.  

**Recomendação Final:**  
Evite permitir que atributos sensíveis sejam manipulados via requisições de escrita. Se for necessário expor essas propriedades em leituras (GET), assegure-se de que estejam bloqueadas para alterações (PUT/PATCH). Sempre que possível, filtre esses campos no API Gateway, BFF ou camada de façade antes que cheguem à lógica da aplicação.  
[+informações referente a vulnerabilidade API-3.](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization)

---

### API-4 - Unrestricted Resource Consumption
*Uso excessivo e não limitado de recursos.*  
**Descrição:** Consumo excessivo de recursos.

**Simulação:** Solicitação de milhares de registros sem limite.
- 🔓 Vulnerável:
  ```bash
  curl "http://localhost:8000/api4/items?limit=10000" -H "X-Secure-Mode: false"
  ```
- 🔐 Seguro:
  ```bash
  curl "http://localhost:8000/api4/items?limit=10000" -H "X-Secure-Mode: true"
  ```
**Conclusão:** No modo seguro, é imposto limite de 100 registros.  

**Recomendação Final:**  
Evite controlar limites diretamente na aplicação. Utilize um API Gateway ou BFF/Facade para aplicar políticas unificadas de consumo. Implemente mecanismos como rate limiting, payload size limit, spike arrest e timeout enforcement para proteger seus recursos contra abusos e sobrecarga.  
[+informações referente a vulnerabilidade API-4.](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption)

---

### API-5 - Broken Function Level Authorization
*Permissões incorretas para diferentes funções.*  
**Descrição:** Controle inadequado de autorização em funções administrativas.

**Simulação:** Usuário comum tenta executar uma função restrita (excluir outro usuário).
- 🔓 Vulnerável:
  ```bash
  curl -X DELETE http://localhost:8000/api5/admin/delete-user/3 -H "X-User-ID: 2" -H "X-Secure-Mode: false"
  ```
- 🔐 Seguro:
  ```bash
  curl -X DELETE http://localhost:8000/api5/admin/delete-user/3 -H "X-User-ID: 2" -H "X-Secure-Mode: true"
  ```
**Conclusão:** No modo seguro, apenas usuários com perfil de admin podem executar ações administrativas.  

**Recomendação Final:**  
Não basta validar se o usuário ou aplicação está autenticado — é essencial aplicar controles de autorização específicos para cada recurso e operação. Garanta que todos os endpoints (incluindo actions administrativas) tenham validações explícitas de perfil, função ou escopo de acesso.  
[+informações referente a vulnerabilidade API-5.](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization)

---

### API-6 - Unrestricted Access to Sensitive Business Flows
*Lógica crítica de negócio sem proteção adequada.*  
**Descrição:** Ausência de controle de acesso em fluxos de negócio críticos.

**Simulação:** Finalizar pedidos de outros usuários.
- 🔓 Vulnerável:
  ```bash
  curl -X POST http://localhost:8000/api6/orders/1002/complete -H "X-Secure-Mode: false"
  ```
- 🔐 Seguro:
  ```bash
  curl -X POST http://localhost:8000/api6/orders/1002/complete -H "X-User-ID: 2" -H "X-Secure-Mode: true"
  ```
**Conclusão:** No modo seguro, apenas o proprietário do pedido consegue completar a operação.  

**Recomendação Final:**  
Adote o princípio de Zero Trust Architecture (ZTA) como padrão: negue por padrão e só permita acessos devidamente autenticados e autorizados para o fluxo de negócio solicitado. Centralize essa validação em um API Gateway com Authorization Server, evitando lógica dispersa na aplicação ou backend.  
[+informações referente a vulnerabilidade API-6.](https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows)

---

### API-7 - Server Side Request Forgery (SSRF)
*API acessando recursos internos indevidos.*  
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
- 🔓 Vulnerável:
  ```bash
  curl "http://localhost:8000/api7/fetch-url?target_url=http://127.0.0.1:80" -H "X-Secure-Mode: false"
  ```
- 🔐 Seguro:
  ```bash
  curl "http://localhost:8000/api7/fetch-url?target_url=http://127.0.0.1:80" -H "X-Secure-Mode: true"
  ```
**Conclusão:** No modo seguro, URLs internas são bloqueadas.  

**Recomendação Final:**  
Sempre valide rigorosamente URLs externas recebidas via API. SSRF pode ser explorado para acessar serviços internos ou metadados de cloud. Bloqueie chamadas para localhost, IPs reservados (127.0.0.1, 10.0.0.0/8, 192.168.0.0/16, entre outros) e monitore destinos suspeitos em tempo de execução.  
[+informações referente a vulnerabilidade API-7.](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery)

---

### API-8 - Security Misconfiguration
*Configurações inseguras no ambiente de API.*  
**Descrição:** Configurações inseguras como debug ativo e ausência de headers de segurança.

**Simulação:** Expor informações sensíveis no debug.
- 🔓 Vulnerável:
  ```bash
  curl http://localhost:8000/api8/debug -H "X-Secure-Mode: false"
  ```
- 🔐 Seguro:
  ```bash
  curl -i http://localhost:8000/api8/debug -H "X-Secure-Mode: true"
  ```
**Conclusão:** No modo seguro, oculta detalhes técnicos e aplica headers de segurança.  

**Recomendação Final:**  
Evite expor mensagens de erro detalhadas ou stack traces ao cliente. Exceções não tratadas corretamente podem revelar informações sensíveis da infraestrutura. Em produção, desative o modo debug e implemente handlers que retornem respostas genéricas ao usuário, mantendo os detalhes restritos aos logs internos.  
[+informações referente a vulnerabilidade API-8.](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration)

---

### API-9 - Improper Inventory Management
*Falta de controle e documentação de endpoints.*  
**Descrição:** Endpoints internos ou antigos não documentados permanecem acessíveis.

**Simulação:** Acesso a endpoints internos e legados.
- 🔓 Vulnerável:
  ```bash
  curl http://localhost:8000/api9/internal/config -H "X-Secure-Mode: false"
  ```
  ```bash
  curl http://localhost:8000/api9/v1/legacy-endpoint -H "X-Secure-Mode: false"
  ```
- 🔐 Seguro:
  ```bash
  curl http://localhost:8000/api9/internal/config -H "X-Secure-Mode: true"
  ```
  ```bash
  curl http://localhost:8000/api9/v1/legacy-endpoint -H "X-Secure-Mode: true"
  ```
**Conclusão:** No modo seguro, rotas internas são escondidas ou desativadas.  

**Recomendação Final:**  
Mantenha um inventário completo e atualizado das APIs expostas — incluindo versões, rotas públicas, internas e deprecated. Remova endpoints obsoletos, oculte rotas administrativas e aplique autenticação e autorização consistentes em toda a superfície de exposição.  
[+informações referente a vulnerabilidade API-9.](https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management)

---

### API-10 - Unsafe Consumption of APIs
*Confiar cegamente em APIs de terceiros.*  
**Descrição:** Confiar cegamente em APIs de terceiros sem validação.

**Pré-requisito:**  Para executar esta DEMO, é necessário:  
1º) Se cadastrar no site: https://www.weatherapi.com;  
2º) [Logar](https://www.weatherapi.com/login.aspx) no site;  
3º) Pegar a existente ou gerar uma nova "API Key".  

**Simulação:** Consumir resposta externa sem validar estrutura.
- 🔓 Vulnerável:
  ```bash
  curl "http://localhost:8000/api10/external/weather?city=Sao Paulo&api_key=SUA_API_KEY" -H "X-Secure-Mode: false"
  ```
- 🔐 Seguro:
  ```bash
  curl "http://localhost:8000/api10/external/weather?city=Sao Paulo&api_key=SUA_API_KEY" -H "X-Secure-Mode: true"
  ```
**Conclusão:** No modo seguro, apenas campos esperados são aceitos.  

**Recomendação Final:**  
APIs de terceiros são fontes potenciais de falhas e ataques — elas podem mudar, retornar dados inválidos ou até serem comprometidas. Nunca consuma dados externos sem validação rigorosa de estrutura e conteúdo. Sempre que possível, use um proxy ou API Gateway para aplicar inspeção e sanitização centralizada.  
[+informações referente a vulnerabilidade API-10.](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis)

---

📢 Criei uma pasta chamada "tests" e coloquei o arquivo da collection Postman com todos os cenários descritos acima. É só baixar e rodar no [Postman](https://postman.com/).  ✔️  

---

## 📄 Autor

Desenvolvido por **Fabrício Alves** para o evento **APIX 2025** ([link do evento](https://www.sensedia.com.br/apix)), palestra "*10 formas de invadir sua API - e como impedir todas elas*" no palco "*Campfire*".

Conecte-se comigo no [LinkedIn](https://www.linkedin.com/in/fabriciocastelar/)!

---

# Let's hack — and fix — APIs the right way! 🛡️🚀