# 👾 NullAccess

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=28&pause=1000&color=00FF99&center=true&vCenter=true&width=500&lines=ACCESS://NULL;SYSTEM+BREACH+DETECTED;INITIALIZING..." />
</p>

> **Invasão de sistema não autorizada detectada.**
> *Você realmente deseja continuar?*

<img src=".prints\logo.png" style="width: 100%; max-width:100%; height: auto;" title="Access://Null logo">

---

## 🎮 Sobre o jogo

**NullAccess** é um jogo de suspense/horror com estética retrô e temática hacker, desenvolvido em Python utilizando Pygame.

Seu objetivo é explorar um sistema corrompido, coletar arquivos secretos e encontrar a saída… enquanto algo te observa nos corredores.

---

## ⚠️ Objetivo

* 📁 Colete todos os **DataFiles**
* 🚪 Encontre a saída
* 👁️ Evite as entidades
* 💀 Não seja pego

<img src=".prints\jogo.png" style="width: 100%; max-width:100%; height: auto;" title="Print da gameplay">

---

## 🕹️ Controles

| Tecla     | Ação         |
| --------- | ------------ |
| `W A S D` | Movimentação |
| `SPACE`   | Iniciar jogo |
| `ESC`     | Fechar jogo  |

---

## 🖥️ Tecnologias Utilizadas

* Python
* Pygame

---

## 📦 Como baixar e executar

### Baixando o Release
Caso você não tenha interesse em fazer todos as etapas abaixo, você pode entrar na aba de <a href="https://github.com/PlopesK/NullAccess/releases/tag/Demo">Releases</a>
e baixar o arquivo "NullAccess.rar"!

### 🔹 Clonando o repositório

```bash
git clone https://github.com/PlopesK/NullAccess.git
cd NullAccess
```

---

### 🔹 Criando ambiente virtual

```bash
python -m venv venv
```

---

### 🔹 Ativando ambiente virtual

#### Windows (PowerShell)

```powershell
venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

---

### 🔹 Instalando dependências

```bash
pip install pygame
```

---

### 🔹 Executando o jogo

```bash
python src/main.py
```

---

## 🚀 Build (.exe)

Para gerar o executável:

```powershell
python -m PyInstaller `
--onedir `
--noconsole `
--add-data "assets;assets" `
src/main.py
```

O executável será criado em:

```txt
dist/main/
```

---

> *“O sistema está instável...”*

---

## 👨‍💻 Desenvolvido por

Gabriel Primo

> *“Nem todo acesso deveria ser permitido.”*

<img src=".prints\gameover.png" style="width: 100%; max-width:100%; height: auto;" title="Fim de jogo">
