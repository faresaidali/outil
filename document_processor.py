from docx import Document
import PyPDF2
from PyPDF2 import PdfReader
import openai

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QTextEdit, QFileDialog, QMessageBox, QInputDialog, QScrollArea

class DocumentProcessorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Document Processor")

        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.input_button = QPushButton("Télécharger un fichier")
        self.input_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.input_button)

        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)

        self.summary_button = QPushButton("Résumer")
        self.summary_button.clicked.connect(self.summarize_content)
        self.layout.addWidget(self.summary_button)

        self.setCentralWidget(self.central_widget)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionnez un fichier")
        if file_path:
            try:
                content = self.read_file_content(file_path)
                self.text_edit.setPlainText(content)
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Une erreur est survenue lors de la lecture du fichier : {e}")

    def read_file_content(self, file_path):
        content = ""
        if file_path.endswith('.docx'):
            doc = Document(file_path)
            content = ' '.join(paragraph.text for paragraph in doc.paragraphs)
        elif file_path.endswith('.pdf'):
            pdf_file_obj = open(file_path, 'rb')
            pdf_reader = PdfReader(pdf_file_obj)
            content = ""
            for page_obj in pdf_reader.pages:
                content += page_obj.extract_text()
            pdf_file_obj.close()
        elif file_path.endswith('.txt'):
            with open(file_path, "r") as file:
                content = file.read()
        else:
            QMessageBox.critical(self, "Erreur", "Type de fichier non pris en charge. Veuillez fournir un fichier .docx, .pdf ou .txt.")
        return content

    def summarize_content(self):
        content = self.text_edit.toPlainText()
        if content:
            # Configuration de l'API OpenAI
            openai.api_key = "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"
            prompt = "Resumes moi ce document en plusieurs points compréhensibles pour un développeur : "
            max_tokens = 10000  # Limite de caractères pour chaque résumé

            # Découper le texte en morceaux plus petits
            chunks = [content[i:i+max_tokens] for i in range(0, len(content), max_tokens)]

            # Résumé du contenu
            summarized_content = ""
            for chunk in chunks:
                # Appel à l'API OpenAI ChatGPT pour chaque chunk
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[{"role": "user", "content": prompt + chunk}]
                )

                # Récupérer la réponse générée par ChatGPT
                response = completion.choices[0].message["content"]
                print(response)

                summarized_content += response.strip() + " "

            summarized_content = summarized_content.replace("\n", "<br/>") # Remplacer les sauts de ligne par des balises HTML

            summary_label = QLabel()
            summary_label.setTextFormat(QtCore.Qt.RichText)
            summary_label.setText("Résumé du contenu :<br/>" + summarized_content)
            summary_label.setWordWrap(True)
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(summary_label)
            self.layout.addWidget(scroll_area)
        else:
            QMessageBox.warning(self, "Avertissement", "Veuillez télécharger un fichier ou entrer du texte.")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    dp_window = DocumentProcessorWindow()
    dp_window.show()
    app.exec_()
