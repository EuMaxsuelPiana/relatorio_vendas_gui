# -*- coding: utf-8 -*-
import os
import sys

# Adicionar o diretório pai ao sys.path para permitir import relativo
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.gui import RelatorioApp

def main():
    """Função principal para iniciar a aplicação."""
    # Garantir que o diretório de saída exista
    output_dir_main = os.path.abspath(os.path.join(parent_dir, "output"))
    if not os.path.exists(output_dir_main):
        os.makedirs(output_dir_main)

    # Garantir que __init__.py exista no src
    src_dir = os.path.join(parent_dir, "src")
    init_path = os.path.join(src_dir, "__init__.py")
    if not os.path.exists(init_path):
        try:
            with open(init_path, "w") as f:
                pass
        except OSError as e:
            print(f"Aviso: Não foi possível criar {init_path}. Erro: {e}")

    # Inicia a interface gráfica
    app = RelatorioApp()
    app.mainloop()

if __name__ == "__main__":
    main()
