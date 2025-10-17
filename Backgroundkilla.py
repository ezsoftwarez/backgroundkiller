import tkinter as tk
from tkinter import filedialog, colorchooser, ttk
from PIL import Image
import threading
import os

# --- LOCALIZATION DATA ---
LOCALIZED_STRINGS = {
    'title': {'hu': "Háttér Eltávolító (Tömeges)", 'en': "Background Remover (Batch)", 'de': "Hintergrund Entferner (Stapel)", 'pl': "Usuwanie Tła (Masowe)", 'ja': "背景除去 (一括)", 'zh': "背景去除 (批量)", 'ar': "إزالة الخلفية (مجمعة)", 'hi': "बैकग्राउंड रिमूवर (बैच)", 'uk': "Видалення фону (Пакетне)", 'ru': "Удаление фона (Пакетное)", 'es': "Removedor de Fondo (Lote)", 'fr': "Suppresseur d'arrière-plan (Lot)"},
    'target_color': {'hu': "Eltávolítandó Célszín:", 'en': "Target Color to Remove:", 'de': "Zielfarbe Entfernen:", 'pl': "Kolor docelowy:", 'ja': "対象色:", 'zh': "目标颜色:", 'ar': "اللون المستهدف:", 'hi': "लक्ष्य रंग:", 'uk': "Цільовий колір:", 'ru': "Целевой цвет:", 'es': "Color Objetivo:", 'fr': "Couleur Cible:"},
    # Tip now uses the word 'Picker' to clarify it's a dialog, not a full eyedropper
    'picker_tip': {'hu': "Szín Választása (Kattints a párbeszédablak megnyitásához)", 'en': "Pick Color (Click to open Color Picker dialog)", 'de': "Farbe Wählen (Klicken, um den Dialog zu öffnen)", 'pl': "Wybierz Kolor (Kliknij, aby otworzyć dialog)", 'ja': "色を選択 (クリックしてダイアログを開く)", 'zh': "选择颜色 (点击打开颜色选择器)", 'ar': "اختيار اللون (انقر لفتح مربع حوار)", 'hi': "रंग चुनें (डायलॉग खोलने के लिए क्लिक करें)", 'uk': "Вибрати колір (Клікніть, щоб відкрити діалог)", 'ru': "Выбрать цвет (Нажмите, чтобы открыть диалог)", 'es': "Elegir Color (Clic para abrir diálogo)", 'fr': "Choisir Couleur (Clic pour ouvrir le dialogue)"},
    'tolerance': {'hu': "Tolerancia (0 - 100):", 'en': "Tolerance (0 - 100):", 'de': "Toleranz (0 - 100):", 'pl': "Tolerancja (0 - 100):", 'ja': "許容範囲 (0 - 100):", 'zh': "容差 (0 - 100):", 'ar': "التسامح (0 - 100):", 'hi': "सहिष्णुता (0 - 100):", 'uk': "Толерантність (0 - 100):", 'ru': "Допуск (0 - 100):", 'es': "Tolerancia (0 - 100):", 'fr': "Tolérance (0 - 100):"},
    'browse_files': {'hu': "Fájlok Tallózása...", 'en': "Browse Files...", 'de': "Dateien Durchsuchen...", 'pl': "Przeglądaj Pliki...", 'ja': "ファイルを参照...", 'zh': "浏览文件...", 'ar': "تصفح الملفات...", 'hi': "फ़айлें ब्राउज़ करें...", 'uk': "Огляд файлів...", 'ru': "Обзор файлов...", 'es': "Examinar Archivos...", 'fr': "Parcourir Fichiers..."},
    'files_selected': {'hu': "{count} fájl kiválasztva", 'en': "{count} files selected", 'de': "{count} Dateien ausgewählt", 'pl': "Wybrano {count} plików", 'ja': "{count}個のファイルを選択済み", 'zh': "已选择 {count} 个文件", 'ar': "تم اختيار {count} ملفات", 'hi': "{count} फाइलें चयनित", 'uk': "Вибрано {count} файлів", 'ru': "Выбрано {count} файлов", 'es': "{count} archivos seleccionados", 'fr': "{count} fichiers sélectionnés"},
    'output_dir': {'hu': "Kimeneti mappa:", 'en': "Output Directory:", 'de': "Ausgabeordner:", 'pl': "Katalog Wyjściowy:", 'ja': "出力ディレクトリ:", 'zh': "输出目录:", 'ar': "مجلد الإخراج:", 'hi': "आउटपुट निर्देशिका:", 'uk': "Вихідний каталог:", 'ru': "Выбрать каталог", 'es': "Directorio de Salida:", 'fr': "Dossier de Sortie:"},
    'select_dir': {'hu': "Mappa Kiválasztása", 'en': "Select Directory", 'de': "Ordner Wählen", 'pl': "Wybierz Katalog", 'ja': "ディレクトリを選択", 'zh': "选择目录", 'ar': "تحديد المجلد", 'hi': "निर्देशिका चुनें", 'uk': "Вибрати каталог", 'ru': "Выбрать каталог", 'es': "Seleccionar Directorio", 'fr': "Sélectionner Dossier"},
    'process_button': {'hu': "FELDOLGOZÁS ÉS MENTÉS", 'en': "PROCESS AND SAVE", 'de': "VERARBEITEN UND SPEICHERN", 'pl': "PRZETWARZAJ I ZAPISZ", 'ja': "処理して保存", 'zh': "处理并保存", 'ar': "معالجة وحفظ", 'hi': "संसाधित करें और सहेजें", 'uk': "ОБРОБИТИ ТА ЗБЕРЕГТИ", 'ru': "ОБРАБОТАТЬ И СОХРАНИТЬ", 'es': "PROCESAR Y GUARDAR", 'fr': "TRAITER ET SAUVEGARDER"},
    'error_files': {'hu': "Hiba: Válasszon ki fájlokat!", 'en': "Error: Select files!", 'de': "Fehler: Dateien auswählen!", 'pl': "Błąd: Wybierz pliki!", 'ja': "エラー: ファイルを選択してください!", 'zh': "错误：选择文件！", 'ar': "خطأ: حدحدد الملفات!", 'hi': "त्रुटि: फ़ाइलें चुनें!", 'uk': "Помилка: Виберіть файли!", 'ru': "Ошибка: Выберите файлы!", 'es': "Error: Seleccione archivos!", 'fr': "Erreur: Sélectionnez fichiers!"},
    'error_dir': {'hu': "Hiba: Válasszon ki kimeneti mappát!", 'en': "Error: Select output directory!", 'de': "Fehler: Ausgabeordner auswählen!", 'pl': "Błąd: Wybierz katalog wyjściowy!", 'ja': "エラー: 出力ディレクトリを選択してください!", 'zh': "错误：选择输出目录！", 'ar': "خطأ: حدد مجلد الإخراج!", 'hi': "त्रुटि: आउटपुट निर्देशिका चुनें!", 'uk': "Помилка: Виберіть вихідний каталог!", 'ru': "Ошибка: Выберите выходной каталог!", 'es': "Error: Seleccione directorio de salida!", 'fr': "Erreur: Sélectionnez dossier de sortie!"},
    'processing_start': {'hu': "Feldolgozás elindítva...", 'en': "Processing started...", 'de': "Verarbeitung gestartet...", 'pl': "Rozpoczęto przetwarzanie...", 'ja': "処理開始...", 'zh': "开始处理...", 'ar': "بدأت المعالجة...", 'hi': "प्रोसेसिंग शुरू हो गई है...", 'uk': "Обробка розпочата...", 'ru': "Обработка началась...", 'es': "Procesamiento iniciado...", 'fr': "Traitement démarré..."},
    'processing_file': {'hu': "Feldolgozás: {idx}/{total} - {name}", 'en': "Processing: {idx}/{total} - {name}", 'de': "Verarbeitung: {idx}/{total} - {name}", 'pl': "Przetwarzanie: {idx}/{total} - {name}", 'ja': "処理中: {idx}/{total} - {name}", 'zh': "正在处理: {idx}/{total} - {name}", 'ar': "المعالجة: {idx}/{total} - {name}", 'hi': "प्रोसेसिंग: {idx}/{total} - {name}", 'uk': "Обробка: {idx}/{total} - {name}", 'ru': "Обработка: {idx}/{total} - {name}", 'es': "Procesando: {idx}/{total} - {name}", 'fr': "Traitement: {idx}/{total} - {name}"},
    'file_error': {'hu': "Hiba történt a fájl feldolgozásakor. Lásd a konzolt.", 'en': "Error occurred during file processing. See console.", 'de': "Error occurred during file processing. See console.", 'pl': "Błąd przetwarzania. Zobacz konsolę.", 'ja': "処理エラー。コンソールを参照。", 'zh': "处理出错。请查看控制台。", 'ar': "حدث خطأ. انظر وحدة التحكم.", 'hi': "प्रोसेसिंग त्रुटि। कंसोल देखें।", 'uk': "Помилка обробки. Див. консоль.", 'ru': "Ошибка обработки. См. консоль.", 'es': "Error de procesamiento. Ver consola.", 'fr': "Erreur de traitement. Voir console."},
    'finished': {'hu': "Kész! {processed}/{total} kép feldolgozva.", 'en': "Done! {processed}/{total} images processed.", 'de': "Fertig! {processed}/{total} Bilder verarbeitet.", 'pl': "Gotowe! Przetworzono {processed}/{total} obrazów.", 'ja': "完了！ {processed}/{total}枚の画像を処理済み。", 'zh': "完成！ 已处理 {processed}/{total} 张图像。", 'ar': "انتهى! تم معالجة {processed}/{total} صورة.", 'hi': "हो गया! {processed}/{total} इमेज प्रोसेस की गईं।", 'uk': "Готово! Оброблено {processed}/{total} зображень.", 'ru': "Готово! Обработано {processed}/{total} изображений.", 'es': "¡Hecho! {processed}/{total} imágenes procesadas.", 'fr': "Terminé ! {processed}/{total} images traitées."},
    'language_selector': {'hu': "Nyelv:", 'en': "Language:", 'de': "Sprache:", 'pl': "Język:", 'ja': "言語:", 'zh': "语言:", 'ar': "لغة:", 'hi': "भाषा:", 'uk': "Мова:", 'ru': "Язык:", 'es': "Idioma:", 'fr': "Langue:"},
    'file_types': {'hu': "Képfájlok", 'en': "Image Files", 'de': "Bilddateien", 'pl': "Pliki Obrazów", 'ja': "画像ファイル", 'zh': "图像文件", 'ar': "ملفات الصور", 'hi': "छवि फ़ाइलें", 'uk': "Файли зображень", 'ru': "Файлы изображений", 'es': "Archivos de Imagen", 'fr': "Fichiers Image"}
}

# Default background color (white)
TARGET_COLOR = (255, 255, 255)
DEFAULT_TOLERANCE = 15 # Default tolerance

class BackgroundRemoverApp:
    def __init__(self, master):
        self.master = master
        
        # Language setup
        self.language_options = {
            "Magyar": 'hu', "English": 'en', "Deutsch": 'de', "Polski": 'pl', "日本語": 'ja', 
            "中文": 'zh', "العربية": 'ar', "हिन्दी": 'hi', "Українська": 'uk', "Русский": 'ru', 
            "Español": 'es', "Français": 'fr'
        }
        # SET DEFAULT LANGUAGE TO ENGLISH
        self.current_language = tk.StringVar(value='en') 
        self.current_language.trace_add("write", self.update_ui_texts_callback)
        
        # Auto-size window
        master.title(self.get_text('title'))
        
        self.input_files = [] 
        self.output_dir = tk.StringVar(value=os.getcwd())
        
        self.target_color_rgb = list(TARGET_COLOR) 
        self.tolerance_value = tk.DoubleVar(value=DEFAULT_TOLERANCE) 
        
        # --- Create Elements ---

        # 0. Language Selector
        self.lang_frame = tk.Frame(master)
        self.lang_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.lang_label = tk.Label(self.lang_frame, text="")
        self.lang_label.pack(side=tk.LEFT)
        
        lang_keys = list(self.language_options.keys())
        # Set default value in the selector to "English"
        self.lang_selector = ttk.Combobox(self.lang_frame, values=lang_keys, textvariable=tk.StringVar(value="English"), state="readonly")
        self.lang_selector.bind("<<ComboboxSelected>>", self.set_language_from_selector)
        self.lang_selector.pack(side=tk.RIGHT)
        
        # 1. Target Color Display and Picker Icon
        self.color_frame = tk.Frame(master)
        self.color_frame.pack(pady=10)

        self.color_label = tk.Label(self.color_frame, text="")
        self.color_label.pack(side=tk.LEFT, padx=5)
        
        # Color Display Box - Clickable
        self.color_display = tk.Label(self.color_frame, text="      ", bg=self._rgb_to_hex(self.target_color_rgb), relief=tk.RAISED, width=3, height=1, cursor="hand2")
        self.color_display.pack(side=tk.LEFT, padx=(5, 10))
        self.color_display.bind("<Button-1>", lambda e: self.choose_color()) # Bind click to color display

        # Eyedropper Icon (Unicode character: Up-pointing triangle with two parallel horizontal lines)
        # Using a pipette symbol (U+1F453 - Eyeglasses, but used here as placeholder) or another Unicode that resembles a tool.
        # I'll use a simpler, common pipette-like character for better compatibility: \u21B6 (North West Arrow to Long Bar) or \u2692 (Hammer and Pick)
        # Let's use \u25BE (Black right-pointing small triangle) with a contrasting background
        
        # We will use the common Unicode for Eyedropper: \u25C9 (Fisheye) or similar, but the most visually recognizable is a small square icon.
        # Let's use the Unicode for a pipette \U0001F4CD (Pushpin) as a placeholder for the tool look, or use a font icon. 
        # Since we can't rely on FontAwesome, we stick to a symbolic representation.
        # Using a very simple 'E' for Eyedropper, styled as a button
        self.eyedropper_icon = tk.Button(self.color_frame, text=" \u25b6 ", font=('Arial', 12, 'bold'), command=self.choose_color, fg="#555", cursor="hand2", relief=tk.FLAT, bd=0, bg=master.cget('bg'))
        # Using \u29bf (Circled dot operator) as a target icon instead of a heavy symbol
        self.eyedropper_icon.config(text="\u267A", font=('Arial', 14, 'bold')) # Recycling symbol as a tool
        self.eyedropper_icon.pack(side=tk.LEFT, padx=0)
        
        # Tip label (explains the click)
        self.picker_tip_label = tk.Label(self.color_frame, text="", fg="#555")
        self.picker_tip_label.pack(side=tk.LEFT, padx=5)
        
        # 2. Tolerance Slider
        self.tolerance_label_frame = tk.Frame(master)
        self.tolerance_label_frame.pack(fill=tk.X, padx=20, pady=(10,0))
        self.tolerance_label = tk.Label(self.tolerance_label_frame, text="", anchor=tk.W)
        self.tolerance_label.pack(side=tk.LEFT)
        self.tolerance_value_label = tk.Label(self.tolerance_label_frame, text=f"{self.tolerance_value.get():.0f}")
        self.tolerance_value_label.pack(side=tk.RIGHT)
        
        self.tolerance_slider = ttk.Scale(master, from_=0.0, to=100.0, variable=self.tolerance_value, orient=tk.HORIZONTAL, command=self._update_tolerance_value)
        self.tolerance_slider.pack(fill=tk.X, padx=20)
        
        # 3. Input Files
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(pady=15, padx=20, fill=tk.X)
        
        self.browse_button = tk.Button(self.input_frame, text="", command=self.select_input_files, bg="#ADD8E6")
        self.browse_button.pack(side=tk.LEFT)
        self.file_count_label = tk.Label(self.input_frame, text="")
        self.file_count_label.pack(side=tk.RIGHT, padx=5)

        # 4. Output Directory
        self.output_dir_frame = tk.Frame(master)
        self.output_dir_frame.pack(pady=5, padx=20, fill=tk.X)
        
        self.output_label = tk.Label(self.output_dir_frame, text="")
        self.output_label.pack(side=tk.LEFT)
        tk.Entry(self.output_dir_frame, textvariable=self.output_dir, width=25, state='readonly').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.select_dir_button = tk.Button(self.output_dir_frame, text="", command=self.select_output_directory, bg="#FFFACD")
        self.select_dir_button.pack(side=tk.RIGHT)

        # 5. Process Button
        self.process_button = tk.Button(master, text="", command=self.start_processing, bg="#90EE90", height=2, font=('Arial', 10, 'bold'))
        self.process_button.pack(pady=20, padx=20, fill=tk.X)

        # 6. Progress Bar and Status
        self.progressbar = ttk.Progressbar(master, orient="horizontal", length=300, mode="indeterminate")
        self.status_label = tk.Label(master, text="", fg="blue")
        self.status_label.pack(pady=5)
        
        # Initial UI update
        self.update_ui_texts()
        self.update_file_count_label(0)


    def get_text(self, key):
        """Returns the localized string for the current language."""
        lang = self.current_language.get()
        # Fallback to English if the current language is not available for a specific key
        return LOCALIZED_STRINGS.get(key, {}).get(lang, LOCALIZED_STRINGS.get(key, {}).get('en', f"MISSING TEXT: {key}"))


    def set_language_from_selector(self, event):
        """Sets the current language based on the selected Combobox value."""
        selected_key = self.lang_selector.get()
        new_lang_code = self.language_options.get(selected_key)
        if new_lang_code:
            self.current_language.set(new_lang_code)

    def update_ui_texts_callback(self, *args):
        """Callback for StringVar change (when language is switched)"""
        self.update_ui_texts()

    def update_ui_texts(self):
        """Updates all text elements in the GUI."""
        # Window title
        self.master.title(self.get_text('title'))
        
        # Language Selector
        self.lang_label.config(text=self.get_text('language_selector'))
        
        # Color
        self.color_label.config(text=self.get_text('target_color'))
        self.picker_tip_label.config(text=self.get_text('picker_tip'))
        
        # Tolerance
        self.tolerance_label.config(text=self.get_text('tolerance'))

        # Input Files
        self.browse_button.config(text=self.get_text('browse_files'))
        self.update_file_count_label(len(self.input_files))

        # Output Directory
        self.output_label.config(text=self.get_text('output_dir'))
        self.select_dir_button.config(text=self.get_text('select_dir'))

        # Process Button
        self.process_button.config(text=self.get_text('process_button'))

    def update_file_count_label(self, count):
        """Updates the label showing the number of selected files."""
        text = self.get_text('files_selected').format(count=count)
        self.file_count_label.config(text=text)

    def _rgb_to_hex(self, rgb):
        """Converts an RGB list to a HEX string for Tkinter."""
        return f'#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}'

    def _update_tolerance_value(self, value):
        """Updates the display of the tolerance slider value."""
        self.tolerance_value_label.config(text=f"{float(value):.0f}")

    def choose_color(self):
        """Opens the color chooser dialog."""
        # Note: This is the system color picker. It can't sample colors outside its dialog box.
        color_code = colorchooser.askcolor(title=self.get_text('picker_tip'))
        if color_code and color_code[0]: 
            self.target_color_rgb = [int(c) for c in color_code[0]]
            hex_color = color_code[1] 
            self.color_display.config(bg=hex_color)

    def select_input_files(self):
        """Opens the file dialog to select input images (multiple files)."""
        file_types_text = self.get_text('file_types')
        f_types = [(file_types_text, '*.png *.jpg *.jpeg *.gif *.bmp *.tiff'), (file_types_text, '*.*')]
        paths = filedialog.askopenfilenames(filetypes=f_types)
        if paths:
            self.input_files = list(paths)
            self.update_file_count_label(len(self.input_files))

    def select_output_directory(self):
        """Opens the directory selector for the output folder."""
        path = filedialog.askdirectory()
        if path:
            self.output_dir.set(path)

    def start_processing(self):
        """Starts the processing in a separate thread."""
        if not self.input_files:
            self.status_label.config(text=self.get_text('error_files'), fg="red")
            return
        if not self.output_dir.get():
            self.status_label.config(text=self.get_text('error_dir'), fg="red")
            return

        # Disable controls and show progress bar
        self.process_button.config(state=tk.DISABLED)
        self.color_display.unbind("<Button-1>") # Disable click on color box
        self.eyedropper_icon.config(state=tk.DISABLED) # Disable icon button
        self.progressbar.pack(pady=10)
        self.progressbar.start()
        self.status_label.config(text=self.get_text('processing_start'), fg="blue")

        # Run the long operation on a separate thread
        processing_thread = threading.Thread(target=self.process_images_threaded)
        processing_thread.start()

    def process_images_threaded(self):
        """The actual image processing logic that runs on a separate thread."""
        processed_count = 0
        total_files = len(self.input_files)
        target_color = tuple(self.target_color_rgb)
        tolerance = self.tolerance_value.get()
        output_dir = self.output_dir.get()
        
        # Local variables for thread (localized text)
        processing_file_text = self.get_text('processing_file')
        file_error_text = self.get_text('file_error')

        for i, input_path in enumerate(self.input_files):
            try:
                import os
                base_name = os.path.basename(input_path)
                name_without_ext = os.path.splitext(base_name)[0]
                output_path = os.path.join(output_dir, f"{name_without_ext}_transparent.png")

                # Update status on the main GUI thread
                status_text = processing_file_text.format(idx=i+1, total=total_files, name=base_name)
                self.master.after(0, lambda text=status_text: self.status_label.config(text=text, fg="blue"))
                
                # Open and convert image to RGBA (for Alpha channel)
                img = Image.open(input_path).convert("RGBA")
                datas = img.getdata()

                new_data = []
                for item in datas:
                    r, g, b, a = item
                    
                    r_diff = abs(r - target_color[0])
                    g_diff = abs(g - target_color[1])
                    b_diff = abs(b - target_color[2])

                    # Remove if the color is within tolerance
                    if r_diff <= tolerance and g_diff <= tolerance and b_diff <= tolerance:
                        new_data.append((255, 255, 255, 0)) # Make it transparent (Alpha = 0)
                    else:
                        new_data.append(item)

                img.putdata(new_data)
                # Save as PNG to preserve transparency
                img.save(output_path, "PNG") 
                processed_count += 1

            except Exception as e:
                print(f"Error processing file {input_path}: {e}")
                self.master.after(0, lambda: self.status_label.config(text=file_error_text, fg="red"))
                
        # Restore GUI state after processing
        self.master.after(0, self.processing_finished, processed_count, total_files)

    def processing_finished(self, processed_count, total_files):
        """Restores the GUI state after processing is complete."""
        self.progressbar.stop()
        self.progressbar.pack_forget() 
        self.process_button.config(state=tk.NORMAL)
        
        # Re-enable click events
        self.color_display.bind("<Button-1>", lambda e: self.choose_color())
        self.eyedropper_icon.config(state=tk.NORMAL)
        
        # Display the "finished" message
        finished_text = self.get_text('finished').format(processed=processed_count, total=total_files)
        self.status_label.config(text=finished_text, fg="green")


# --- Main program execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()
