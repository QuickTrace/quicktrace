# Quicktrace

Introducing QuickTrace, the ultimate AI-powered semantic search tool designed to empower journalists and 
revolutionize investigative reporting. With QuickTrace, journalists can swiftly navigate through vast repositories
of project assets, including video, audio, PDFs, and text, to uncover hidden connections and crucial evidence. 
Harnessing cutting-edge artificial intelligence, QuickTrace accelerates the investigative process, 
providing journalists with lightning-fast access to critical information. Maximize efficiency, uncover the truth,
and elevate your investigations with QuickTrace—the trusted companion of every 
journalist committed to impactful and comprehensive reporting.

## Connecting to Google Drive
Enable your Google Drive API by following the instructions [here](https://developers.google.com/drive/api/quickstart/python). Save the `credentials.json` file in the top level directory.

To download all files from your Google Drive account to be uploaded to QuickTrace,
run `python google_drive.py`. 

To search for a specific filetype, use `python -c "from google_drive import search_filetype('filename.ext')"`
