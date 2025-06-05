🧾 Gerador de Relatórios de Vendas

Aplicativo em Python com interface gráfica que permite:

✅ Selecionar arquivos CSV de vendas  
📊 Gerar relatórios com gráficos e estatísticas  
📤 Exportar os resultados para PDF e Excel  
📧 Enviar relatórios automaticamente por e-mail

Este projeto também inclui um guia completo para empacotar o app como um executável `.exe` utilizando **PyInstaller**, para que funcione em qualquer computador com Windows, mesmo sem Python instalado.

---

## 📁 Estrutura do Projeto

relatorio_vendas_gui/
├── main.py
├── requirements.txt
├── README.md
├── src/
│ ├── interface.py
│ ├── relatorio.py
│ ├── exportacao.py
│ └── email_sender.py

---

## ✅ Pré-requisitos

Antes de empacotar o aplicativo como `.exe`, verifique os seguintes itens:

- **Python 3 instalado**  
  [🔗 Baixe aqui](https://www.python.org/downloads/)  
  > Marque a opção **"Add Python to PATH"** durante a instalação

- **pip atualizado**
  ```bash
  python -m pip install --upgrade pip
