# RR-simulator

Aplicação gráfica em Python para simulação e visualização interativa do algoritmo de escalonamento de CPU **Round Robin** (Preemptivo por fatia de tempo).

---

## 🚀 Funcionalidades

* **Acompanhamento em Tempo Real:** Tabela dinâmica que exibe os processos da fila e atualiza o tempo restante a cada segundo.
* **Adição Dinâmica:** Adicione novos processos com diferentes tempos de execução a qualquer momento, mesmo durante a simulação.
* **Quantum Configurável:** Ajuste o valor do *Time Slice* (fatia de tempo) antes de iniciar a execução.
* **Controles Interativos:** Botões para iniciar e interromper a simulação de forma segura.
* **Interface Não-Bloqueante:** Processamento baseado em *multithreading*, garantindo que a janela continue responsiva sem travar a interface gráfica.

---

## 🛠️ Pré-requisitos

O programa requer **Python 3** e a biblioteca gráfica **Tkinter**.

Em distribuições Linux, o pacote do Tkinter deve ser instalado separadamente:

* **Fedora:**
  ```bash
  sudo dnf install python3-tkinter

## 📋 Como Usar
Definir o Quantum: Ajuste o campo Time Slice (s) com o tempo máximo de CPU por processo.

Inserir Processos: Digite a duração total do processo em Tempo do Processo (s) e clique em + Adicionar.

Iniciar Escalonamento: Clique no botão ▶ Iniciar Execução.

Interagir: É possível adicionar novos processos durante o processamento ou clicar em ⏹ Interromper para pausar.

## 📂 Arquitetura do Projeto
rr2.py: Versão principal com interface gráfica construída em Tkinter e gerenciamento de concorrência com a biblioteca threading.

Nota: Esta documentação descreve a versão com interface gráfica (rr2.py). O repositório também conta com o arquivo rr.py, no qual o escalonador Round Robin é implementado de uma forma mais grosseira e direta no terminal, utilizando leituras via teclado e sem uso de bibliotecas de interface visual.
