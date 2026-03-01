# 🎰 Máquina de Cassino

Jogo de caça-níquel no terminal feito em Python.

## Como jogar

1. Clone o repositório ou baixe o `main.py`
2. Rode o arquivo:
```bash
python main.py
```
3. Digite seu nome e comece a apostar!

## Funcionalidades

- Saldo inicial de R$ 100 por jogador
- Apostas configuráveis (mínimo R$ 5)
- Animação de giro no terminal
- Salvamento automático do saldo entre sessões
- Suporte a múltiplos jogadores no mesmo arquivo
- Estatísticas da sessão (total ganho, perdido, jogadas)

## Prêmios

| Combinação | Prêmio |
|---|---|
| 💎💎💎 | Jackpot — 10x a aposta |
| 💥💥💥 | Super prêmio — 5x a aposta |
| 🔥🔥🔥 / 💣💣💣 / ⚠️⚠️⚠️ | 3x a aposta |
| Dois iguais | 2x a aposta |

## Tecnologias

- Python 3
- Bibliotecas padrão: `random`, `json`, `time`, `os`
