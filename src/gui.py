import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
from datetime import datetime
import traceback # Para logs de erro mais detalhados

# Importar módulos locais
from . import processador
from . import exportador
from . import emailer # Importar o módulo emailer

# --- Janela de Configuração de E-mail ---
class EmailConfigWindow(tk.Toplevel):
    def __init__(self, parent, attachment_path_suggestion=None):
        super().__init__(parent)
        self.parent = parent
        self.title("Configurar Envio de E-mail")
        self.geometry("450x450") # Ajustar tamanho conforme necessário
        self.transient(parent) # Mantém a janela sobre a principal
        self.grab_set() # Bloqueia interação com a janela principal

        # --- Variáveis --- 
        self.smtp_server = tk.StringVar(value="smtp.gmail.com") # Sugestão comum
        self.smtp_port = tk.StringVar(value="587") # Porta padrão TLS
        self.sender_email = tk.StringVar()
        self.sender_password = tk.StringVar()
        self.recipient_email = tk.StringVar()
        self.subject = tk.StringVar(value=f"Relatório de Vendas - {datetime.now().strftime(\"%d/%m/%Y\")}")
        self.body = tk.StringVar(value="Segue em anexo o relatório de vendas gerado.")
        self.attachment_path = tk.StringVar(value=attachment_path_suggestion or "")

        # --- Layout --- 
        frame = ttk.Frame(self, padding="10")
        frame.pack(expand=True, fill=tk.BOTH)

        # Campos de configuração SMTP
        ttk.Label(frame, text="Servidor SMTP:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.smtp_server, width=40).grid(row=0, column=1, pady=2)

        ttk.Label(frame, text="Porta SMTP:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.smtp_port, width=10).grid(row=1, column=1, sticky=tk.W, pady=2)

        ttk.Label(frame, text="Seu E-mail (Remetente):").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.sender_email, width=40).grid(row=2, column=1, pady=2)

        ttk.Label(frame, text="Sua Senha/App Password:").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.sender_password, show="*", width=40).grid(row=3, column=1, pady=2)

        ttk.Label(frame, text="E-mail do Destinatário:").grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.recipient_email, width=40).grid(row=4, column=1, pady=2)

        ttk.Label(frame, text="Assunto:").grid(row=5, column=0, sticky=tk.W, pady=2)
        ttk.Entry(frame, textvariable=self.subject, width=40).grid(row=5, column=1, pady=2)

        ttk.Label(frame, text="Corpo do E-mail:").grid(row=6, column=0, sticky=tk.NW, pady=2)
        tk.Text(frame, height=4, width=40).grid(row=6, column=1, pady=2) # Usar Text para corpo maior
        # Associar Text widget com StringVar é mais complexo, vamos pegar o valor diretamente no envio
        self.body_text_widget = frame.grid_slaves(row=6, column=1)[0]
        self.body_text_widget.insert(tk.END, self.body.get())

        # Campo e botão para selecionar anexo
        ttk.Label(frame, text="Anexo:").grid(row=7, column=0, sticky=tk.W, pady=2)
        entry_anexo = ttk.Entry(frame, textvariable=self.attachment_path, width=30, state=\"readonly\")
        entry_anexo.grid(row=7, column=1, sticky=tk.W, pady=2)
        btn_select_anexo = ttk.Button(frame, text="Selecionar...", command=self.select_attachment)
        btn_select_anexo.grid(row=7, column=1, sticky=tk.E, padx=5)

        # Botão de Enviar
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Enviar E-mail", command=self.send).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def select_attachment(self):
        # Sugerir diretório de saída
        initial_dir = self.parent.output_dir
        file_path = filedialog.askopenfilename(
            title="Selecione o Relatório para Anexar",
            initialdir=initial_dir,
            filetypes=[("Arquivos PDF", "*.pdf"), ("Arquivos Excel", "*.xlsx"), ("Todos os arquivos", "*.*")]
        )
        if file_path:
            self.attachment_path.set(file_path)

    def send(self):
        # Obter valores dos campos
        server = self.smtp_server.get()
        try:
            port = int(self.smtp_port.get())
        except ValueError:
            messagebox.showerror("Erro", "Porta SMTP inválida. Deve ser um número.", parent=self)
            return
        sender = self.sender_email.get()
        password = self.sender_password.get()
        recipient = self.recipient_email.get()
        subject = self.subject.get()
        body = self.body_text_widget.get("1.0", tk.END).strip() # Obter do Text widget
        attachment = self.attachment_path.get()

        # Validações básicas
        if not all([server, port, sender, password, recipient, subject, body]):
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos obrigatórios.", parent=self)
            return
        if attachment and not os.path.exists(attachment):
             messagebox.showwarning("Aviso", f"Arquivo de anexo não encontrado: {attachment}", parent=self)
             return

        # Tentar enviar
        try:
            # Mostrar mensagem de "enviando"
            status_label = ttk.Label(self, text="Enviando e-mail...", foreground="blue")
            status_label.pack(pady=5)
            self.update_idletasks() # Forçar atualização da UI

            emailer.enviar_email_com_anexo(
                server, port, sender, password, recipient, subject, body, attachment
            )
            messagebox.showinfo("Sucesso", "E-mail enviado com sucesso!", parent=self.parent) # Mostrar na janela principal
            self.destroy() # Fechar janela de configuração

        except (ConnectionRefusedError, ConnectionAbortedError, FileNotFoundError) as e:
             messagebox.showerror("Erro de Conexão/Arquivo", str(e), parent=self)
        except Exception as e:
            messagebox.showerror("Erro ao Enviar", f"Ocorreu um erro inesperado: {e}\n\nVerifique os detalhes do SMTP, a senha (use senha de app se tiver 2FA) e sua conexão.", parent=self)
            # Log detalhado no console para debug
            print("--- ERRO DETALHADO NO ENVIO DE EMAIL ---")
            traceback.print_exc()
            print("-----------------------------------------")
        finally:
            # Remover mensagem de status
            if \'status_label\' in locals() and status_label.winfo_exists():
                status_label.destroy()

# --- Classe Principal da Aplicação ---
class RelatorioApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerador de Relatórios de Vendas")
        self.geometry("800x600")

        # --- Diretório de Saída Padrão ---
        self.output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.last_exported_file = None # Guardar caminho do último arquivo exportado

        # --- Estilo --- 
        style = ttk.Style(self)
        style.theme_use("clam")

        # --- Layout Principal --- 
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # --- Frame de Controles (Botões) --- 
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.btn_select_file = ttk.Button(control_frame, text="Selecionar Arquivo CSV", command=self.select_file)
        self.btn_select_file.pack(side=tk.LEFT, padx=5)

        self.btn_generate_report = ttk.Button(control_frame, text="Gerar Relatório", command=self.generate_report, state=tk.DISABLED)
        self.btn_generate_report.pack(side=tk.LEFT, padx=5)

        self.btn_export_pdf = ttk.Button(control_frame, text="Exportar PDF", command=self.export_pdf, state=tk.DISABLED)
        self.btn_export_pdf.pack(side=tk.LEFT, padx=5)

        self.btn_export_excel = ttk.Button(control_frame, text="Exportar Excel", command=self.export_excel, state=tk.DISABLED)
        self.btn_export_excel.pack(side=tk.LEFT, padx=5)

        self.btn_send_email = ttk.Button(control_frame, text="Enviar por E-mail", command=self.open_email_config, state=tk.DISABLED) # Alterado comando
        self.btn_send_email.pack(side=tk.LEFT, padx=5)

        # --- Frame de Exibição de Dados --- 
        data_frame = ttk.LabelFrame(main_frame, text="Resultados do Relatório", padding="10")
        data_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.lbl_file_path = ttk.Label(data_frame, text="Arquivo selecionado: Nenhum")
        self.lbl_file_path.pack(anchor=tk.W)

        self.lbl_faturamento = ttk.Label(data_frame, text="Faturamento Total: R$ 0.00")
        self.lbl_faturamento.pack(anchor=tk.W)

        self.lbl_produto_mais_vendido = ttk.Label(data_frame, text="Produto Mais Vendido: -")
        self.lbl_produto_mais_vendido.pack(anchor=tk.W)

        self.lbl_total_itens = ttk.Label(data_frame, text="Total de Itens Vendidos: 0")
        self.lbl_total_itens.pack(anchor=tk.W)

        # --- Frame para o Gráfico --- 
        self.chart_frame = ttk.Frame(main_frame)
        self.chart_frame.pack(expand=True, fill=tk.BOTH, pady=5)
        self.canvas_widget = None
        self.display_chart(None)

        # --- Variáveis de Estado --- 
        self.file_path = None
        self.report_data = None
        self.dataframe = None
        self.chart_figure = None

    def select_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Selecione o arquivo CSV",
            filetypes=(("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*"))
        )
        if self.file_path:
            self.lbl_file_path.config(text=f"Arquivo selecionado: {os.path.basename(self.file_path)}")
            self.btn_generate_report.config(state=tk.NORMAL)
            self.reset_report_state()
        else:
            self.lbl_file_path.config(text="Arquivo selecionado: Nenhum")
            self.btn_generate_report.config(state=tk.DISABLED)
            self.reset_report_state()

    def reset_report_state(self):
        self.btn_export_pdf.config(state=tk.DISABLED)
        self.btn_export_excel.config(state=tk.DISABLED)
        self.btn_send_email.config(state=tk.DISABLED)
        self.lbl_faturamento.config(text="Faturamento Total: R$ 0.00")
        self.lbl_produto_mais_vendido.config(text="Produto Mais Vendido: -")
        self.lbl_total_itens.config(text="Total de Itens Vendidos: 0")
        self.report_data = None
        self.dataframe = None
        self.last_exported_file = None # Limpar último exportado
        self.display_chart(None)

    def generate_report(self):
        if not self.file_path:
            messagebox.showwarning("Aviso", "Nenhum arquivo CSV selecionado.")
            return

        try:
            self.dataframe = processador.processar_csv(self.file_path)
            self.report_data = processador.calcular_metricas(self.dataframe)

            self.lbl_faturamento.config(text=f"Faturamento Total: R$ {self.report_data["faturamento"]:.2f}")
            self.lbl_produto_mais_vendido.config(text=f"Produto Mais Vendido: {self.report_data["mais_vendido"]}")
            self.lbl_total_itens.config(text=f"Total de Itens Vendidos: {self.report_data["total_itens"]}")

            self.display_chart(self.report_data.get("vendas_por_produto"))

            self.btn_export_pdf.config(state=tk.NORMAL)
            self.btn_export_excel.config(state=tk.NORMAL)
            self.btn_send_email.config(state=tk.NORMAL)
            self.last_exported_file = None # Resetar último exportado ao gerar novo relatório

        except FileNotFoundError as e:
            messagebox.showerror("Erro de Arquivo", str(e))
            self.reset_report_state()
        except ValueError as e:
            messagebox.showerror("Erro de Dados", str(e))
            self.reset_report_state()
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao gerar o relatório: {e}")
            traceback.print_exc() # Log detalhado
            self.reset_report_state()

    def display_chart(self, vendas_data):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        self.canvas_widget = None
        if self.chart_figure:
             plt.close(self.chart_figure)
             self.chart_figure = None

        if vendas_data is None or vendas_data.empty:
            lbl_chart_placeholder = ttk.Label(self.chart_frame, text="Área do Gráfico (sem dados)", relief=tk.SUNKEN, anchor=tk.CENTER)
            lbl_chart_placeholder.pack(expand=True, fill=tk.BOTH)
            return

        try:
            top_n = 10
            vendas_plot = vendas_data.nlargest(top_n)

            self.chart_figure, ax = plt.subplots(figsize=(7, 4))
            vendas_plot.plot(kind="bar", ax=ax)
            ax.set_title(f"Top {top_n} Produtos Mais Vendidos (Quantidade)")
            ax.set_xlabel("Produto")
            ax.set_ylabel("Quantidade Vendida")
            ax.tick_params(axis="x", rotation=45, labelsize=8)
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(self.chart_figure, master=self.chart_frame)
            self.canvas_widget = canvas.get_tk_widget()
            self.canvas_widget.pack(expand=True, fill=tk.BOTH)
            canvas.draw()

        except Exception as e:
            messagebox.showerror("Erro de Gráfico", f"Não foi possível gerar o gráfico: {e}")
            traceback.print_exc()
            lbl_chart_placeholder = ttk.Label(self.chart_frame, text="Erro ao gerar gráfico", relief=tk.SUNKEN, anchor=tk.CENTER)
            lbl_chart_placeholder.pack(expand=True, fill=tk.BOTH)
            self.chart_figure = None

    def export_pdf(self):
        if not self.report_data:
            messagebox.showwarning("Aviso", "Gere um relatório primeiro antes de exportar.")
            return

        default_filename = f"relatorio_vendas_{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}.pdf"
        save_path = filedialog.asksaveasfilename(
            title="Salvar Relatório PDF como...",
            initialdir=self.output_dir,
            initialfile=default_filename,
            defaultextension=".pdf",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
        )

        if save_path:
            try:
                exportador.exportar_para_pdf(self.report_data, self.chart_figure, save_path)
                self.last_exported_file = save_path # Guardar caminho
                messagebox.showinfo("Sucesso", f"Relatório PDF salvo com sucesso em:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Erro ao Exportar PDF", f"Não foi possível salvar o PDF: {e}")
                traceback.print_exc()

    def export_excel(self):
        if not self.report_data or self.dataframe is None:
            messagebox.showwarning("Aviso", "Gere um relatório primeiro antes de exportar.")
            return

        default_filename = f"relatorio_vendas_{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}.xlsx"
        save_path = filedialog.asksaveasfilename(
            title="Salvar Relatório Excel como...",
            initialdir=self.output_dir,
            initialfile=default_filename,
            defaultextension=".xlsx",
            filetypes=[("Arquivos Excel", "*.xlsx"), ("Todos os arquivos", "*.*")]
        )

        if save_path:
            try:
                exportador.exportar_para_excel(self.report_data, self.dataframe, self.chart_figure, save_path)
                self.last_exported_file = save_path # Guardar caminho
                messagebox.showinfo("Sucesso", f"Relatório Excel salvo com sucesso em:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Erro ao Exportar Excel", f"Não foi possível salvar o Excel: {e}")
                traceback.print_exc()

    def open_email_config(self):
        if not self.report_data:
            messagebox.showwarning("Aviso", "Gere um relatório primeiro antes de enviar.")
            return
        
        # Sugerir o último arquivo exportado como anexo
        EmailConfigWindow(self, attachment_path_suggestion=self.last_exported_file)

# --- Ponto de Entrada --- 
# (Será movido para main.py posteriormente)
if __name__ == "__main__":
    # Garantir que __init__.py exista
    src_dir = os.path.dirname(__file__)
    init_path = os.path.join(src_dir, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            pass
    # Garantir que o diretório de saída exista
    output_dir_main = os.path.abspath(os.path.join(src_dir, "..", "output"))
    if not os.path.exists(output_dir_main):
        os.makedirs(output_dir_main)

    app = RelatorioApp()
    app.mainloop()
