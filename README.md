# SourceCheckup

This is the repo for the data and code used in the paper [How well do LLMs cite relevant medical references? An evaluation framework and analyses](https://arxiv.org/abs/2402.02008)

## Data

The data are contained in the following Google Drive: [link](https://drive.google.com/drive/folders/1a-i974g3XzLCtZLpTLBbqAwK0olpd5JY?usp=drive_link)
The files are organized as follows:
  - Questions: The 1200 questions used in this analysis. The original documents from Mayo Clinic, UpToDate, and r/AskDocs used to generate each question are not included here due to terms of use for each site. However, the questions generated from each page are available in questions.csv.
  - Responses: The responses for each of the seven models are provided within each CSV in the Responses folder.
  - Parsed Statements: Each response is parsed for medically relevant statements, which are included as a list within a column.
  - Fact-Citation Pairs: The facts are paired with citations provided to back each response.
