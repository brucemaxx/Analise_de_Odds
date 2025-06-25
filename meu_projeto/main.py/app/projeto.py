# Configurações sensíveis e parâmetros de negócio
import random

# Solicita o token e o chat_id pelo terminal
TELEGRAM_TOKEN = input("Digite o TOKEN do seu bot Telegram: ").strip()
TELEGRAM_CHAT_ID = input("Digite o CHAT_ID do Telegram: ").strip()
ODDS_THRESHOLD = 1.2  # Odds 20% acima da média são consideradas valiosas
REFRESH_INTERVAL = 60  # Intervalo entre coletas de odds (em segundos)

def fetch_mock_odds():
    """
    Simula retorno de odds com formato semelhante a uma API.
    """
    events = [
        {
            'event': 'Time A x Time B',
            'market': 'Vencedor da partida',
            'odds': {
                'Time A': round(random.uniform(1.5, 2.3), 2),
                'Empate': round(random.uniform(2.5, 4.0), 2),
                'Time B': round(random.uniform(1.5, 2.5), 2)
            }
        }
    ]
    return events

# Sistema de alerta via Telegram
from telegram import Bot

bot = Bot(token=TELEGRAM_TOKEN)

def verificar_valor(evento):
    """
    Analisa as odds e envia alertas se houver valor.
    """
    resultados = []
    try:
        mercado = evento['market']
        odds = evento['odds']
        media = sum(odds.values()) / len(odds)
        for selecao, odd in odds.items():
            if odd > media * ODDS_THRESHOLD:
                mensagem = (
                    f"*Alerta de Valor*\n"
                    f"Evento: {evento['event']}\n"
                    f"Mercado: {mercado}\n"
                    f"Seleção: {selecao}\n"
                    f"Odd: {odd} (média: {round(media, 2)})"
                )
                print("==== ALERTA GERADO ====")
                print(mensagem)
                print("=======================")
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mensagem, parse_mode='Markdown')
                resultados.append({'evento': evento['event'], 'selecao': selecao, 'odd': odd})
    except Exception as e:
        print(f"[ERRO ALERTA] {e}")
    return resultados

# Logger de histórico em CSV
import csv
from datetime import datetime

def salvar_no_csv(evento):
    """
    Registra os eventos analisados no CSV para fins de histórico/backtest.
    """
    try:
        with open('historico.csv', mode='a', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            for selecao, odd in evento['odds'].items():
                writer.writerow([datetime.now(), evento['event'], evento['market'], selecao, odd])
    except Exception as e:
        print(f"[ERRO CSV] {e}")

# Função principal de monitoramento
import time

def iniciar_monitoramento():
    """
    Função principal: busca odds, analisa valor, salva histórico e repete o ciclo.
    """
    print("🟢 Monitoramento iniciado...")
    while True:
        eventos = fetch_mock_odds()
        for evento in eventos:
            verificar_valor(evento)
            salvar_no_csv(evento)
        time.sleep(REFRESH_INTERVAL)

if __name__ == "__main__":
    iniciar_monitoramento()
