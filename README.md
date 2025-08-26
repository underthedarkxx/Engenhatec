# 💡 EngenhaTech

EngenhaTech é uma plataforma educacional voltada para a divulgação de conteúdos técnicos e materiais educativos. O sistema conta com um site responsivo (frontend) e uma API REST segura (backend) que permite autenticação de usuários, acesso a materiais e um sistema de chat exclusivo para assinantes.

## 🧩 Funcionalidades

### Frontend
- Landing page responsiva com informações introdutórias
- Telas de login e cadastro com integração visual
- Navegação entre páginas com layout unificado

### Backend
- API RESTful com Flask
- Autenticação com JWT (login, registro e rota `/me`)
- Sistema de chat com verificação de assinatura
- CRUD completo de materiais
- FAQ exclusivo para assinantes

## 🛠 Tecnologias Utilizadas

### Frontend
- HTML5 / CSS3 / JavaScript

### Backend
- Python 3 / Flask
- Flask-JWT-Extended
- SQLAlchemy + SQLite
- Bcrypt para criptografia de senhas

## 📂 Estrutura de Pastas

```
engenhatech/
├── backend/
│   ├── routes/
│   ├── models/
│   ├── utils/
│   ├── config.py
│   ├── __init__.py
│   └── app.py
├── frontend/
│   ├── static/
│   └── templates/
└── README.md
```

## 🚀 Como Executar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/underthedarkxx/engenhatech.git
   cd engenhatech
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Instale as dependências do backend:**
   ```bash
   (venv) ...$ pip freeze > requirements.txt
   ```

4. **Execute a aplicação:**
   ```bash
   python backend/app.py
   ```

5. **Acesse no navegador:**
   ```
   http://localhost:5000
   ```

## 👥 Equipe de Desenvolvimento

### Frontend
- Pedro Henrique
- Luiz Fernando
- Daniel Matos

### Backend
- Roberto Dias
- Mateus Fonseca
- Matheus Santana

## 📅 Cronograma de Entregas

| Etapa                         | Data       |
|------------------------------|------------|
| Entrega da landing page      | 22/05/2025 |
| Telas de login e cadastro    | 25/05/2025 |
| Reestruturação da landing    | 27/05/2025 |
| Entrega final (frontend + backend) | 29/05/2025 |

## 📜 Licença

Este projeto é de uso acadêmico e está sob a Licença MIT.
