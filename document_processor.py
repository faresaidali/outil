import openai_api

class DocumentProcessor:
    def __init__(self):
        self.summarized_content = ""

    def process_input(self):
        # Code for uploading a file or entering text manually goes here

    def summarize_content(self, content):
        # Use the OpenAI API to summarize the content
        self.summarized_content = openai_api.summarize(content)
