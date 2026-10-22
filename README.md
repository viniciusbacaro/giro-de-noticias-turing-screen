# Giro de Notícias — Turing Smart Screen

Painel de notícias internacionais para a Turing Smart Screen de 3,5", desenvolvido em Python e executado no Ubuntu.

O programa consulta o feed RSS do G1 Mundo, apresenta manchetes em uma interface gráfica própria e atualiza a tela periodicamente.

## Funcionalidades

- Manchetes internacionais do G1 Mundo.
- Atualização periódica.
- Interface gráfica de 480 × 320 pixels.
- Exibição de horário e data.
- Execução automática por meio do systemd do usuário.
- Reinício automático do programa em caso de falha.

## Requisitos

- Ubuntu ou distribuição Linux compatível.
- Python 3 e `python3-venv`.
- Tela Turing Smart Screen compatível com a biblioteca utilizada.
- Conexão USB com a tela.
- Acesso à internet.

**Atenção:** nem toda tela LCD de 3,5" é compatível. Confira a revisão e o modelo do seu dispositivo na documentação da biblioteca original.

## Fonte das notícias

Feed RSS do G1 Mundo:

https://g1.globo.com/rss/g1/mundo/

O funcionamento depende da disponibilidade e do formato de resposta desse serviço externo.

## Biblioteca utilizada

O projeto utiliza como base a biblioteca:

https://github.com/mathoudebine/turing-smart-screen-python

A biblioteca original é distribuída sob GNU GPL v3 ou posterior. Consulte o arquivo `LICENSE` e os avisos de autoria para conhecer as condições aplicáveis à redistribuição.

## Instalação

### 1. Instale os requisitos do sistema

```bash
sudo apt update
sudo apt install git python3 python3-venv python3-pip
```

### 2. Obtenha o projeto

Clone o repositório publicado e entre na pasta:

```bash
git clone https://github.com/viniciusbacaro/giro-de-noticias-turing-screen.git
cd giro-de-noticias-turing-screen
```

### 3. Configure o ambiente Python

As dependências devem ser instaladas conforme as instruções da biblioteca original e as necessidades do script:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Configure e execute

Antes da primeira execução, confirme que a biblioteca reconhece sua revisão de tela e que a porta serial está correta. O script deste projeto utiliza `/dev/ttyACM0` como porta padrão.

Ajuste a constante `PORTA` em `noticias.py` se o dispositivo aparecer em outra porta.

Execute:

```bash
python noticias.py
```

## Inicialização automática

A instalação do serviço systemd pode ser configurada após confirmar o caminho final do projeto e do ambiente virtual.

O serviço usado no ambiente original executa `noticias.py` com o Python de `.venv` e está configurado para reiniciar em caso de falha.

## Diagnóstico

Verificar o serviço:

```bash
systemctl --user status giro-noticias.service --no-pager
```

Consultar os registros:

```bash
journalctl --user -u giro-noticias.service -n 50 --no-pager
```

## Aviso

Projeto pessoal e independente, sem afiliação oficial com o G1 ou com o fabricante da tela.

## Autor

Vinicius Gabriel

## Licença

A distribuição deste projeto deve respeitar a licença da biblioteca original e os avisos de autoria dos componentes utilizados. As condições específicas para os arquivos próprios do projeto devem ser definidas antes da publicação.

