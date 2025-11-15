# ☁️ Painel Meteorológico Dinâmico com Flask

Um painel de controle interativo e responsivo para visualização de dados climáticos em tempo real, utilizando a API Open-Meteo.  
O dashboard demonstra boas práticas de desenvolvimento, focando na organização modular do código Python e CSS, e na apresentação clara das informações.

![Demonstração](docs/demonstracao.gif)
---

## ✨ Funcionalidades Principais

- **Busca Geográfica:** Pesquisa dinâmica por nome de cidade, utilizando Geocoding para obter coordenadas, fuso horário e nome em Português.  
- **Design Responsivo:** Layout adaptável para desktop e dispositivos móveis.  
- **Dados Detalhados:** Exibe temperatura atual, umidade, pressão, velocidade e direção do vento.  
- **Previsão Horária:** Gráfico interativo (Chart.js) da temperatura nas próximas 24 horas.  
- **Previsão Semanal:** Visualização simplificada das máximas e mínimas para os próximos 7 dias.  
- **Cache Inteligente:** Implementação de um cache simples em memória (5 minutos) no serviço (`weather_service.py`) para reduzir chamadas repetitivas à API.  

---

## 🛠️ Tecnologias Utilizadas

### Backend (Python)

| Módulo        | Descrição |
|---------------|-----------|
| Flask         | Micro-framework web para roteamento e manipulação de requisições. |
| Requests      | Para fazer requisições HTTP às APIs externas (Open-Meteo). |
| PyTZ / Locale | Manipulação de fusos horários e formatação de datas em Português (pt_BR). |

### Frontend

| Tecnologia    | Descrição |
|---------------|-----------|
| Jinja2        | Motor de template para renderização dinâmica do HTML. |
| Chart.js      | Biblioteca JavaScript para visualização interativa do gráfico horário. |
| CSS (Modular) | Estilos organizados em arquivos lógicos (`base/`, `components/`, `layout/`) para facilitar a manutenção. |

---

## 🏗️ Arquitetura do Projeto

O código Python e o CSS seguem uma estrutura modular para desacoplamento e clareza:

```Painel-Meteorologico-CIAg/
├── app.py                  # Roteamento Flask (Camada de Apresentação)
├── requirements.txt        # Lista de dependências Python
├── services/               # Camada de Negócios e Acesso a Dados
│   ├── api_client.py       # Funções puras para requisições externas (APIs)
│   ├── mapping.py          # Mapeamento de códigos da API para ícones e descrições em Português
│   └── weather_service.py  # Orquestrador: processa dados brutos e implementa lógica de cache
├── static/
│   ├── css/                # Modularização dos estilos
│   │   ├── base/           # Variáveis, cores e reset de estilos
│   │   ├── components/     # Cards, Header, Tooltips
│   │   ├── layout/         # Grids e responsividade
│   │   └── style.css       # Arquivo final linkado no HTML
│   └── js/
│       └── chart.js        # Scripts de gráficos e interatividade
└── templates/
    ├── base.html           # Template base do Jinja2
    └── index.html          # Página principal do painel
```
---

## 📦 Instalação e Execução

### Pré-requisitos

- Python 3.8+
- Conexão à internet para API

### Passo 1: Clonar o repositório

`git clone https://github.com/Lelesouzasilvaa/Painel-Meteorologico-CIAg`
`cd Painel-Meteorologico-CIAg`

### Passo 2: Configurar ambiente virtual
`python -m venv venv`

#### Para ativar (Linux/macOS)
`source venv/bin/activate`

#### Para ativar (Windows - PowerShell)
`.\venv\Scripts\Activate`

### Passo 3: Instalar dependências

`pip install -r requirements.txt`

### Passo 4: Executar a aplicação

`python app.py`

Acesse o painel em: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🔹 Estrutura de Funções no Projeto

- **api_client.py**
  - `geocode_city_name(city_name)` → Busca coordenadas e fuso horário da cidade.
  - `fetch_weather(latitude, longitude, timezone)` → Requisição à API Open-Meteo.
  
- **mapping.py**
  - `map_weather_code_to_icon(code, is_day)` → Converte códigos da API em ícones.
  - `map_weather_code_to_description(code)` → Converte códigos da API em descrições em português.

- **weather_service.py**
  - `get_weather_data(city_name)` → Orquestra dados, organiza o cache e prepara a estrutura para o frontend.
  - `obter_dados_clima(nome_cidade)` → Função de cache em memória para reduzir chamadas repetitivas.

- **app.py**
  - Roteamento Flask: `@app.route('/')` → Captura entrada do usuário, chama `get_weather_data` e renderiza `index.html`.

---

<table>
  <tr>
    <td>
        
## 💡 Observações

- O cache evita múltiplas requisições à API se o mesmo dado for solicitado dentro de 5 minutos.
- O frontend é totalmente responsivo e modular, podendo ser facilmente extendido.
- A visualização horária usa **Chart.js**, podendo ser customizada com cores, estilos e tooltips.
- Todos os dados são atualizados em tempo real e exibidos em Português.

---
## 🎨 Layout e Estilo

- O painel esquerdo contém informações detalhadas do clima e previsão horária.
- O painel direito mostra previsão semanal resumida.
- Cards de vento, umidade, pressão, UV e probabilidade de chuva possuem tooltips e hover animado.
- O CSS é modular e responsivo, permitindo fácil manutenção e escalabilidade.
  </td>
    <td>
<p align="center">
  <img src="docs/demonstracao2.gif" width="300" alt="Demonstração" />
</p>
</table>
