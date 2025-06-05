# Aplicativo de Relatórios de Vendas com GUI

Este é um aplicativo de desktop desenvolvido em Python com uma interface gráfica (GUI) para gerar relatórios diários de vendas a partir de arquivos CSV.

## Funcionalidades

*   **Seleção de Arquivo:** Permite ao usuário selecionar um arquivo CSV contendo dados de vendas. O CSV deve ter as colunas: `data`, `produto`, `quantidade`, `valor_total`.
*   **Processamento de Dados:** Calcula automaticamente:
    *   Faturamento total do dia.
    *   Produto mais vendido (em quantidade).
    *   Quantidade total de itens vendidos.
*   **Visualização:** Exibe os dados processados e um gráfico de barras dos produtos mais vendidos diretamente na interface.
*   **Exportação:** Permite exportar o relatório gerado nos formatos:
    *   PDF
    *   Planilha Excel (.xlsx)
*   **Envio por E-mail:** Permite enviar o relatório gerado (em PDF ou Excel) por e-mail manualmente (requer configuração de SMTP).

**Observação sobre Agendamento:** A funcionalidade de agendamento automático de envio de e-mail não está disponível devido a limitações do ambiente atual. O envio será implementado de forma manual através de um botão na interface.

## Tecnologias Utilizadas

*   **Linguagem:** Python 3
*   **Interface Gráfica (GUI):** Tkinter (biblioteca padrão do Python)
*   **Manipulação de Dados:** Pandas (para leitura e processamento do CSV)
*   **Geração de Gráficos:** Matplotlib
*   **Geração de PDF:** ReportLab
*   **Geração de Planilhas Excel:** openpyxl
*   **Envio de E-mail:** smtplib, email.mime

## Estrutura do Projeto

```
relatorio_vendas_gui/
├── src/             # Código fonte do aplicativo
│   ├── __init__.py
│   ├── main.py        # Ponto de entrada principal
│   ├── gui.py         # Lógica da interface gráfica
│   ├── processador.py # Lógica de processamento de dados e cálculos
│   ├── exportador.py  # Lógica de exportação (PDF, Excel)
│   └── emailer.py     # Lógica de envio de e-mail
├── output/          # Diretório para salvar relatórios exportados
├── requirements.txt # Dependências do projeto
├── todo.md          # Lista de tarefas
└── README.md        # Este arquivo
```

## Próximos Passos

1.  Implementar a interface gráfica básica.
2.  Adicionar a funcionalidade de seleção e leitura do arquivo CSV.
3.  Implementar os cálculos e a geração do gráfico.
4.  Integrar as opções de exportação para PDF e Excel.
5.  Implementar a funcionalidade de envio manual por e-mail.
6.  Fornecer instruções para empacotamento.

---

## ✅ Pré-requisitos

Antes de empacotar o aplicativo como `.exe`, verifique os seguintes itens:

- **Python 3 instalado**  
  [🔗 Baixe aqui](https://www.python.org/downloads/)  
  > Marque a opção **"Add Python to PATH"** durante a instalação

- **pip atualizado**
  ```bash
  python -m pip install --upgrade pip
