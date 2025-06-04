"""Analisa ações brasileiras usando dados públicos do Yahoo Finance.
Gera médias móveis e salva gráficos de cada ativo.
"""
import os
import requests
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def fetch_ibov_tickers() -> list[str]:
    """Return the list of tickers from the Ibovespa index using the brapi API.

    Requires the environment variable ``BRAPI_TOKEN`` with a valid token for
    https://brapi.dev/. The function appends the ``.SA`` suffix used on Yahoo
    Finance to each symbol.
    """
    token = os.environ.get("BRAPI_TOKEN")
    if not token:
        raise RuntimeError(
            "Defina o token de acesso em BRAPI_TOKEN para obter a composicao do IBOV"
        )

    url = "https://brapi.dev/api/quote/%5EBVSP"
    resp = requests.get(url, params={"modules": "composition", "token": token})
    resp.raise_for_status()
    data = resp.json()
    composition = data["results"][0]["composition"]
    return [item["stock"] + ".SA" for item in composition]

# Obtem a lista completa de empresas que compõem o Ibovespa
tickers = fetch_ibov_tickers()

# Baixa os dados de mercado a partir de 2024
start_date = "2024-01-01"

print("Baixando dados de mercado...")
data = yf.download(tickers, start=start_date, auto_adjust=True)

# O objeto retornado possui colunas multi-index (Open, High, Low, Close, etc.)
close_prices = data["Close"]

for ticker in tickers:
    series = close_prices[ticker]
    latest_close = series.iloc[-1]
    mean_price = series.mean()

    print(f"\nTicker: {ticker}")
    print(f"Preço de fechamento mais recente: {latest_close:.2f}")
    print(f"Preço médio desde {start_date}: {mean_price:.2f}")

    ma20 = series.rolling(window=20).mean()
    ma50 = series.rolling(window=50).mean()

    plt.figure(figsize=(10, 6))
    plt.plot(series.index, series, label="Fechamento")
    plt.plot(ma20.index, ma20, label="Média 20 dias")
    plt.plot(ma50.index, ma50, label="Média 50 dias")
    plt.title(f"{ticker} - Preço e Médias Móveis")
    plt.xlabel("Data")
    plt.ylabel("Preço (BRL)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{ticker}_chart.png")
    plt.close()

