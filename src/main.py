
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import genanki
import uuid

class AnkiImageCardCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Anki Image Card Creator")
        self.root.state("zoomed")

        self.theme = "dark"
        self.styles = {
            "dark": {
                "bg": "#1e1e1e",
                "fg": "#f0f0f0",
                "button_bg": "#2d2d2d",
                "button_fg": "#ffffff",
                "canvas": "#2a2a2a"
            },
            "light": {
                "bg": "#f5f5f5",
                "fg": "#000000",
                "button_bg": "#e0e0e0",
                "button_fg": "#000000",
                "canvas": "#ffffff"
            }
        }

        self.image_list = []
        self.current_index = 0
        self.cards = []
        self.tk_img_front = None
        self.tk_img_back = None

        self.setup_ui()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)

        self.theme_button = tk.Button(self.root, text="Alternar Tema", command=self.toggle_theme, font=("Arial", 11, "bold"), height=2, width=15)
        self.theme_button.pack(side='top', pady=5)

        self.image_label = tk.Label(self.main_frame)
        self.image_label.pack()

        self.preview_label = tk.Label(self.main_frame, text="Prévia do Card (Frente e Verso):", font=('Arial', 12, 'bold'))
        self.preview_label.pack(pady=5)

        self.preview_frame = tk.Frame(self.main_frame)
        self.preview_frame.pack(pady=5)

        self.front_canvas = tk.Canvas(self.preview_frame, width=300, height=300)
        self.front_canvas.pack(side='left', padx=10)
        self.back_canvas = tk.Canvas(self.preview_frame, width=300, height=300)
        self.back_canvas.pack(side='right', padx=10)

        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side='bottom', pady=10)

        self.buttons = []
        for label, cmd in [
            ("Abrir Pasta", self.load_images),
            ("Anterior", self.prev_image),
            ("Próxima", self.next_image),
            ("Usar como Frente", lambda: self.add_card('front')),
            ("Usar como Verso", lambda: self.add_card('back')),
            ("Adicionar Áudio", self.add_audio),
            ("Exportar .txt", self.export_txt),
            ("Exportar .apkg", self.export_apkg)
        ]:
            btn = tk.Button(self.controls_frame, text=label, command=cmd, font=("Arial", 11), height=2, width=16)
            btn.pack(side='left', padx=5)
            self.buttons.append(btn)

        self.apply_theme()

    def apply_theme(self):
        style = self.styles[self.theme]
        self.root.configure(bg=style["bg"])
        self.main_frame.configure(bg=style["bg"])
        self.image_label.configure(bg=style["bg"])
        self.preview_label.configure(bg=style["bg"], fg=style["fg"])
        self.preview_frame.configure(bg=style["bg"])
        self.front_canvas.configure(bg=style["canvas"])
        self.back_canvas.configure(bg=style["canvas"])
        self.controls_frame.configure(bg=style["bg"])
        self.theme_button.configure(bg=style["button_bg"], fg=style["button_fg"])
        for btn in self.buttons:
            btn.configure(bg=style["button_bg"], fg=style["button_fg"])

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.apply_theme()

    def load_images(self):
        folder = filedialog.askdirectory()
        if not folder:
            return
        self.image_list = [os.path.join(folder, f) for f in os.listdir(folder)
                           if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
        self.current_index = 0
        if self.image_list:
            self.display_image()
        else:
            messagebox.showinfo("Info", "Nenhuma imagem encontrada na pasta.")

    def display_image(self):
        img_path = self.image_list[self.current_index]
        img = Image.open(img_path)
        img.thumbnail((400, 400))
        self.tk_image = ImageTk.PhotoImage(img)
        self.image_label.configure(image=self.tk_image)

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_image()

    def next_image(self):
        if self.current_index < len(self.image_list) - 1:
            self.current_index += 1
            self.display_image()

    def add_card(self, role):
        path = self.image_list[self.current_index]
        if role == 'front':
            self.cards.append({'front': path, 'back': '', 'audio': ''})
            messagebox.showinfo("Adicionado", "Imagem adicionada como frente.")
        elif role == 'back':
            for card in reversed(self.cards):
                if card['back'] == '':
                    card['back'] = path
                    messagebox.showinfo("Adicionado", "Imagem adicionada como verso.")
                    self.update_preview(card)
                    return
            messagebox.showwarning("Aviso", "Nenhuma frente disponível para associar este verso.")
        self.update_preview(self.cards[-1])

    def add_audio(self):
        audio_path = filedialog.askopenfilename(filetypes=[("Áudio", "*.mp3")])
        if not audio_path:
            return
        for card in reversed(self.cards):
            if card['audio'] == '':
                card['audio'] = audio_path
                messagebox.showinfo("Áudio", f"Áudio adicionado ao último card.")
                self.update_preview(card)
                return
        messagebox.showwarning("Aviso", "Nenhum card disponível para adicionar áudio.")

    def update_preview(self, card):
        self.front_canvas.delete("all")
        self.back_canvas.delete("all")
        if card.get('audio'):
            self.front_canvas.create_text(150, 15, text=f"[sound:{os.path.basename(card['audio'])}]", font=('Arial', 9), anchor='n')
        if card.get('front'):
            img = Image.open(card['front'])
            img.thumbnail((260, 260))
            self.tk_img_front = ImageTk.PhotoImage(img)
            self.front_canvas.create_image(150, 160, image=self.tk_img_front)
        if card.get('back'):
            img = Image.open(card['back'])
            img.thumbnail((260, 260))
            self.tk_img_back = ImageTk.PhotoImage(img)
            self.back_canvas.create_image(150, 160, image=self.tk_img_back)

    def export_txt(self):
        if not self.cards:
            messagebox.showwarning("Aviso", "Nenhum card para exportar.")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("TXT Files", "*.txt")])
        if not output_path:
            return
        export_dir = os.path.dirname(output_path)
        with open(output_path, 'w', encoding='utf-8') as f:
            for card in self.cards:
                front_name = os.path.basename(card['front'])
                shutil.copy(card['front'], os.path.join(export_dir, front_name))
                front_field = f"<img src='{front_name}'>"
                back_field = ''
                if card['back']:
                    back_name = os.path.basename(card['back'])
                    shutil.copy(card['back'], os.path.join(export_dir, back_name))
                    back_field = f"<img src='{back_name}'>"
                if card['audio']:
                    audio_name = os.path.basename(card['audio'])
                    shutil.copy(card['audio'], os.path.join(export_dir, audio_name))
                    front_field = f"[sound:{audio_name}]<br>" + front_field
                f.write(f"{front_field}|{back_field}\n")
        messagebox.showinfo("Sucesso", f"Cards exportados para {output_path}")

    def export_apkg(self):
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        file_path = os.path.join(downloads_path, "deck.apkg")  # Salvamento automático

        model = genanki.Model(
            1607392319,
            'Image and Audio Card Model',
            fields=[
                {'name': 'Front'},
                {'name': 'Back'}
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Front}}',
                    'afmt': '{{Back}}',
                }
            ])

        deck = genanki.Deck(
            int(uuid.uuid4().int >> 64),
            'Deck com Imagem e Áudio'
        )

        media_files = []
        for front, back in self.cards:
            front_html = ""
            back_html = ""

            if front.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                media_files.append(front)
                front_html += f'<img src="{os.path.basename(front)}">'

            elif front.lower().endswith(('.mp3', '.wav', '.ogg', '.wma', '.webm', '.mp4', '.m4a', '.flac', '.wma', '.aac')):
                media_files.append(front)
                front_html += f'<audio controls src="{os.path.basename(front)}"></audio>'

            if back.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                media_files.append(back)
                back_html += f'<img src="{os.path.basename(back)}">'

            elif back.lower().endswith(('.mp3', '.wav', '.ogg', '.wma', '.webm', '.mp4', '.m4a', '.flac', '.wma', '.aac')):
                media_files.append(back)
                back_html += f'<audio controls src="{os.path.basename(back)}"></audio>'

            note = genanki.Note(
                model=model,
                fields=[front_html, back_html]
            )
            deck.add_note(note)

        package = genanki.Package(deck)
        package.media_files = media_files
        package.write_to_file(file_path)

        messagebox.showinfo("Exportado", f"Deck .apkg exportado com sucesso para:
{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnkiImageCardCreator(root)
    root.mainloop()
