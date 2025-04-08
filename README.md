# 📘 Anki Image Card Creator

**Anki Image Card Creator** é um aplicativo criado em Python com interface gráfica que facilita a criação de flashcards personalizados para o Anki, utilizando **imagens, áudios e textos**. O projeto foi desenvolvido com foco em dinamismo, produtividade e simplicidade para estudos.

---

## 🧩 Funcionalidades

- ✅ Interface intuitiva com modo claro/escuro (tema escuro ativado por padrão)
- 🖼️ Visualização de imagens selecionadas em galeria com preview de frente e verso
- 🔊 Suporte a arquivos de áudio vinculados ao card
- ✍️ Exportação automática em:
  - `.txt` no formato `frente|verso` (compatível com importação direta no Anki)
  - `.apkg` com imagens e áudios embutidos
- 💾 Salvamento automático dos arquivos em: `C:\Users\João\Downloads`
- 📥 Geração de arquivos compatíveis com o padrão de flashcards Anki

---

## 🚀 Como Usar

1. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute o app**:
   ```bash
   python src/main.py
   ```

3. **Crie seus cards**:
   - Use os botões para:
     - Selecionar imagens (como frente ou verso)
     - Adicionar áudios
     - Visualizar preview
     - Exportar cards em `.txt` ou `.apkg`

---

## 💡 Formato dos Cards

- **Exportação `.txt`**:
  ```
  frente|verso
  imagem1.jpg|imagem2.jpg
  ```

- **Exportação `.apkg`**:
  - Imagens e áudios são exibidos diretamente no Anki usando HTML:
    ```html
    <audio controls src="audio.mp3"></audio><br><img src="imagem.png">
    ```

---

## 🛠️ Como Empacotar para .exe

Para gerar um executável do app:

1. Certifique-se de que o `PyInstaller` está instalado:
   ```bash
   pip install pyinstaller
   ```

2. Execute:
   ```bash
   pyinstaller main.spec
   ```

3. O executável será gerado na pasta `dist/`.

---

## 🧑‍💻 Sobre o Projeto

- 📌 **Objetivo**: otimizar e dinamizar a criação de flashcards personalizados para estudos pessoais.
- 🛠️ **Tecnologias utilizadas**:
  - `Python`
  - `Tkinter` (interface gráfica)
  - `Pillow` (manipulação de imagens)
  - `genanki` (geração de arquivos `.apkg`)
- 🧪 Desenvolvido com foco em produtividade e usabilidade.

---

## 👤 Autor

Criado por João — para uso pessoal e apoio aos estudos com Anki.