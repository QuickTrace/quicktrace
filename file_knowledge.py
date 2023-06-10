import streamlit as st
import tempfile
from dataclasses import dataclass, field
from typing import Any, List, TypeVar

from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader

from audio_utils import convert_audio_to_text

UploadedFile = TypeVar('UploadedFile', bound=Any)


@dataclass
class FileKnowledge:
    name: str
    file: UploadedFile  # type: ignore # This will hold the uploaded file
    filetype: str  # This will indicate whether the file is a PDF or an audio file
    _content: str = field(default='', repr=False)
    _chunks: List[str] = field(default_factory=list, repr=False)
    splitter: CharacterTextSplitter = field(default_factory=CharacterTextSplitter)

    def __post_init__(self):
        self.content = self.extract_text()
        self.chunks = self.splitter.split_text(self.content)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
        self.save_to_session_state()

    @property
    def chunks(self):
        return self._chunks

    @chunks.setter
    def chunks(self, value):
        self._chunks = value
        self.save_to_session_state()

    def save_to_session_state(self):
        st.session_state.knowledge[self.name] = self

    def extract_text(self):
        if self.filetype == 'pdf':
            return self.extract_text_from_pdf()
        elif self.filetype == 'm4a':
            return self.extract_text_from_audio()
        else:
            raise ValueError(f'Unsupported filetype: {self.filetype}')

    def extract_text_from_pdf(self):
        # Add your code here to extract text from a PDF file
        pdf_reader = PdfReader(self.file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    def extract_text_from_audio(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as tmp:
            tmp.write(self.file.read())
            audio_path = tmp.name
            return convert_audio_to_text(audio_path)
