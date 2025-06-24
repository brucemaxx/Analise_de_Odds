# config.py
# este arquivo armazena variáveis sensíveis e reutilizáveis de forma segura
TELEGRAM_TOKEN = 'SEU_TOKEN_DO_BOT'
TELEGRAM_CHAT_ID = 'SEU_CHAT_ID'

# Defina parâmetros de negócio
ODDS_THRESHOLD = 1.2 # Odds 20% acima da média são consideradas valiosas

# Intervalo entre coletas de odds (em Segundos)
REFRESH_INTERVAL = 60

# bet365_scraper.py
# Aqui simulamos uma coleta de odds (em um projeto real, você faria scraping ou usaria uma API pública/paga)

import random

def fetch_mock_odds():
    """
    Simula retorno de odds com formato semelhante a uma API.
    """
    events = [
        {
            'event': 'Time A x Time B',
            'market': 'Vencedor da partida',
            # 'Average': 1.70,
            'odds': {
                'Time A': round(random.uniform(1.5, 2.3), 2),
                'Empate': round(random.uniform(2.5, 4.0), 2),
                'Time B': round(random.uniform(1.5, 2.5), 2)
            }
        }
    ]
    return events

# alert_system.py
from telegram import Bot # type: ignore
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, ODDS_THRESHOLD

bot = Bot(token=TELEGRAM_TOKEN)

def verificar_valor(evento):
    """
    Analia as odds e envia alertas se houver valor.
    """
    resultados = []
    try:
        mercado = evento['market']
        odds = evento['odds']
        media = sum(odds.value()) / len(odds)
    
    
        for selecao, odd in evento['odds'].items():
            if odd > media * ODDS_THRESHOLD:
                mensagem = (
                    f"*Alerta de Valor*\n"
                    f"Evento: {evento['event']}\n"
                    f"Mercado: {mercado}\n"
                    f"Seleção: {selecao}\n"
                    f"Odd: {odd} (média: {round(media, 2)})"
                )
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mensagem, parse_mode='Markdown')
            resultados.append({'evento': evento['event'], 'selecao': selecao,'odd': odd})
            
    except Exception as e:
        print(f"[ERRO ALERTA] {e}")       
    return resultados



# history_logger.py
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
            


# main.py
import time
from bet365_scraper import fetch_mock_odds
from alert_system import verificar_valor
from history_logger import salvar_no_csv
from config import REFRESH_INTERVAL

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
