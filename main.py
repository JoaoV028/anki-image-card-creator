
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
        self.root.state("zoomed")  # tela cheia
        self.image_list = []
        self.current_index = 0
        self.cards = []
        self.tk_img_front = None
        self.tk_img_back = None
        self.setup_ui()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)

        self.image_label = tk.Label(self.main_frame)
        self.image_label.pack()

        self.preview_label = tk.Label(self.main_frame, text="Prévia do Card (Frente e Verso):", font=('Arial', 12, 'bold'))
        self.preview_label.pack(pady=5)

        self.preview_frame = tk.Frame(self.main_frame, relief='solid', borderwidth=1)
        self.preview_frame.pack(pady=5)

        self.front_canvas = tk.Canvas(self.preview_frame, width=300, height=300, bg='white')
        self.front_canvas.pack(side='left', padx=10)
        self.back_canvas = tk.Canvas(self.preview_frame, width=300, height=300, bg='white')
        self.back_canvas.pack(side='right', padx=10)

        # Botões fixos no final
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(side='bottom', pady=10)

        tk.Button(self.controls_frame, text="Abrir Pasta", command=self.load_images).pack(side='left', padx=5)
        tk.Button(self.controls_frame, text="Anterior", command=self.prev_image).pack(side='left', padx=5)
        tk.Button(self.controls_frame, text="Próxima", command=self.next_image).pack(side='left', padx=5)
        tk.Button(self.controls_frame, text="Usar como Frente", command=lambda: self.add_card('front')).pack(side='left', padx=5)
        tk.Button(self.controls_frame, text="Usar como Verso", command=lambda: self.add_card('back')).pack(side='left', padx=5)
        tk.Button(self.controls_frame, text="Adicionar Áudio", command=self.add_audio).pack(side='left', padx=5)
        tk.Button(self.controls_frame, text="Exportar .txt", command=self.export_txt).pack(side='left', padx=5)
        tk.Button(self.controls_frame, text="Exportar .apkg", command=self.export_apkg).pack(side='left', padx=5)

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
        if not self.cards:
            messagebox.showwarning("Aviso", "Nenhum card para exportar.")
            return
        default_name = os.path.join(os.path.expanduser("~"), "deck_anki_export.apkg")
        output_path = filedialog.asksaveasfilename(initialfile="deck_anki_export.apkg", defaultextension='.apkg', filetypes=[('Anki Deck', '*.apkg')])
        if not output_path:
            return
        model_id = int(uuid.uuid4().int >> 64)
        deck_id = int(uuid.uuid4().int >> 64)
        model = genanki.Model(
            model_id,
            'Image Card Model',
            fields=[{'name': 'Front'}, {'name': 'Back'}],
            templates=[{
                'name': 'Card 1',
                'qfmt': '{{Front}}',
                'afmt': '{{Front}}<hr id="answer">{{Back}}',
            }]
        )
        deck = genanki.Deck(deck_id, 'Image Cards Deck')
        media_files = []
        for card in self.cards:
            front_name = os.path.basename(card['front'])
            media_files.append(card['front'])
            front_html = f'<img src="{front_name}">'
            if card['audio']:
                audio_name = os.path.basename(card['audio'])
                media_files.append(card['audio'])
                front_html = f'[sound:{audio_name}]<br>' + front_html
            back_html = ''
            if card['back']:
                back_name = os.path.basename(card['back'])
                media_files.append(card['back'])
                back_html = f'<img src="{back_name}">'
            note = genanki.Note(model=model, fields=[front_html, back_html])
            deck.add_note(note)
        genanki.Package(deck, media_files=media_files).write_to_file(output_path)
        messagebox.showinfo("Sucesso", f"Deck exportado para {output_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnkiImageCardCreator(root)
    root.mainloop()
