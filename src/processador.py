import pandas as pd

def processar_csv(file_path):
    """Lê um arquivo CSV, valida as colunas e retorna um DataFrame."""
    try:
        df = pd.read_csv(file_path)
        # Validar colunas esperadas
        colunas_esperadas = ['data', 'produto', 'quantidade', 'valor_total']
        if not all(col in df.columns for col in colunas_esperadas):
            raise ValueError(f"O arquivo CSV deve conter as colunas: {', '.join(colunas_esperadas)}")
        
        # Tentar converter colunas para tipos adequados (opcional, mas bom para robustez)
        try:
            df['data'] = pd.to_datetime(df['data'])
            df['quantidade'] = pd.to_numeric(df['quantidade'])
            df['valor_total'] = pd.to_numeric(df['valor_total'])
        except Exception as e:
            raise ValueError(f"Erro ao converter tipos de dados: {e}")

        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Erro: Arquivo não encontrado em {file_path}")
    except pd.errors.EmptyDataError:
        raise ValueError("Erro: O arquivo CSV está vazio.")
    except pd.errors.ParserError:
        raise ValueError("Erro: Falha ao parsear o arquivo CSV. Verifique o formato.")
    except Exception as e:
        raise Exception(f"Ocorreu um erro inesperado ao processar o CSV: {e}")

# Funções de cálculo (serão movidas ou chamadas a partir daqui posteriormente)
def calcular_metricas(df):
    """Calcula as métricas principais a partir do DataFrame."""
    if df is None or df.empty:
        return {
            "faturamento": 0.0,
            "mais_vendido": "-",
            "total_itens": 0,
            "vendas_por_produto": None
        }

    faturamento_total = df['valor_total'].sum()
    total_itens_vendidos = df['quantidade'].sum()
    
    # Agrupar por produto e somar quantidades
    vendas_por_produto = df.groupby('produto')['quantidade'].sum()
    
    produto_mais_vendido = "-"
    if not vendas_por_produto.empty:
        produto_mais_vendido = vendas_por_produto.idxmax()

    return {
        "faturamento": faturamento_total,
        "mais_vendido": produto_mais_vendido,
        "total_itens": total_itens_vendidos,
        "vendas_por_produto": vendas_por_produto # Retorna a série para o gráfico
    }

