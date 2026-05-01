# 🌱 Rede Fazendinha

Sistema de monitoramento agrícola com sensores de umidade do solo, integrando uma rede de sensores sem fio ZigBee/XBee com uma aplicação web Django para visualização e análise dos dados coletados em campo.

---

## 📋 Sobre o Projeto

O **Rede Fazendinha** foi desenvolvido para monitorar em tempo real a umidade do solo em áreas agrícolas. Os sensores instalados no campo transmitem dados via rádio frequência (ZigBee) para um coordenador conectado a um computador, que processa e armazena as leituras em um banco de dados PostgreSQL. Uma interface web permite visualizar a localização dos sensores no mapa, acompanhar o histórico de leituras e exportar os dados para análise.

---

## 🏗️ Arquitetura

```
Sensor de solo → XBee remoto → Coordenador ZigBee (USB/Serial)
                                        ↓
                          rede_xbee_callback.py
                                        ↓
                              PostgreSQL (Heroku)
                                        ↓
                          Aplicação Web Django
                         ┌──────────┬──────────┐
                       Mapa     Dashboard    Tabela/CSV
```

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Django 3.2 + Django REST Framework |
| Banco de dados | PostgreSQL (produção) / SQLite (desenvolvimento) |
| Mapas | django-leaflet + django-geojson |
| Hardware | Módulos XBee/ZigBee (digi-xbee) |
| Deploy | Heroku (gunicorn + whitenoise) |
| Análise de dados | pandas + numpy |

---

## 📁 Estrutura do Projeto

```
rede-fazendinha/
├── geosite/                  # Configurações do projeto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                     # App principal (mapa e templates)
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── infosensor/               # App de sensores e dados
│   ├── models.py             # InfoSensores e InfoDados
│   ├── views.py              # Dashboard, tabela, exportação CSV
│   └── urls.py
├── rede_xbee_callback.py     # Coleta de dados via XBee (ZigBee)
├── verifica_no.py            # Descoberta de nós na rede XBee
├── manage.py
├── requirements.txt
├── Procfile                  # Configuração Heroku
└── runtime.txt               # Versão do Python para Heroku
```

---

## ⚙️ Instalação e Configuração

### Pré-requisitos

- Python 3.9+
- PostgreSQL
- Módulo XBee coordenador conectado via USB (para coleta de dados)

### 1. Clone o repositório

```bash
git clone https://github.com/Antonioufrrj/rede-fazendinha.git
cd rede-fazendinha
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SECRET_KEY=sua_secret_key_aqui
DEBUG=True
DATABASE_URL=postgres://usuario:senha@host:porta/banco
```

### 5. Execute as migrações

```bash
python manage.py migrate
```

### 6. Inicie o servidor

```bash
python manage.py runserver
```

Acesse em: `http://localhost:8000`

---

## 📡 Coleta de Dados via XBee

Para iniciar a coleta de dados dos sensores de campo:

### Verificar nós ativos na rede

```bash
python verifica_no.py
```

Realiza uma varredura de 15 segundos e lista todos os dispositivos XBee detectados.

### Iniciar recepção de dados

```bash
python rede_xbee_callback.py
```

Conecta ao coordenador ZigBee na porta serial configurada e começa a receber e salvar as leituras de capacitância no banco de dados.

> **Configuração da porta serial:** Edite as variáveis `PORT` e `BAUD_RATE` nos scripts conforme a porta do seu sistema (padrão: `COM6`, `9600` baud).

---

## 🌐 Funcionalidades da Interface Web

| Rota | Descrição |
|---|---|
| `/` | Mapa interativo com localização dos sensores |
| `/json:<nome_sensor>/` | Dashboard com gráfico de umidade do sensor |
| `/tables/` | Tabela com todas as leituras |
| `/export_csv` | Download dos dados em formato CSV |
| `/geojson/` | Endpoint GeoJSON com posição dos sensores |
| `/admin/` | Painel administrativo Django |

---

## 🗄️ Modelos de Dados

### InfoSensores
Cadastro dos sensores instalados no campo.

| Campo | Tipo | Descrição |
|---|---|---|
| `nome_sensor` | CharField (PK) | Identificador do sensor (ex: S1, S2) |
| `geom` | PointField | Coordenada GPS (longitude, latitude) |
| `funcao` | CharField | Função do sensor |
| `cultura` | CharField | Cultura monitorada |
| `altitude` | FloatField | Altitude em metros |
| `profundidade` | FloatField | Profundidade de instalação (cm) |
| `cap_campo` | FloatField | Capacidade de campo (%) |
| `murcha_pmt` | FloatField | Ponto de murcha permanente (%) |

### InfoDados
Leituras coletadas pelos sensores.

| Campo | Tipo | Descrição |
|---|---|---|
| `sensor` | ForeignKey | Referência ao sensor |
| `data` | DateField | Data da leitura |
| `hora` | TimeField | Hora da leitura |
| `capacitancia` | FloatField | Valor bruto de capacitância |
| `umidade` | FloatField | Umidade do solo (%) |
| `precipitacao` | FloatField | Precipitação (mm) |

---

## 🚀 Deploy no Heroku

O projeto está configurado para deploy no Heroku com `gunicorn` e `whitenoise` para arquivos estáticos.

```bash
heroku create nome-do-app
heroku addons:create heroku-postgresql:hobby-dev
git push heroku master
heroku run python manage.py migrate
```

---

## ⚠️ Observações de Segurança

- Nunca commite o arquivo `.env` com credenciais reais no repositório
- Mantenha `DEBUG=False` em produção
- Utilize variáveis de ambiente para todas as credenciais do banco de dados

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos e de pesquisa na UFRRJ (Universidade Federal Rural do Rio de Janeiro).
