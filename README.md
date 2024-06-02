# SourceCheckup

This is the repo for the data and code used in the paper 
[How well do LLMs cite relevant medical references? An evaluation framework and analyses](https://arxiv.org/abs/2402.02008)
![alt text](https://github.com/kevinwu23/SourceCheckup/blob/main/fig2.jpg?raw=true)

## Overview
SourceCheckup is a tool designed to verify the accuracy of information extracted from a given citation URL or a direct question. The script processes the provided input, queries an AI model for generating questions and verifying responses, and outputs the results in a CSV file. It also provides insights into the fraction of statements supported by at least one citation.

## Modules

### utils.py
Contains utility functions used in the main script:
- `extract_contents_from_url(citation_url)`: Extracts contents from the given URL.
- `GPTWrapper`: A wrapper for querying the AI model with specified prompts and settings.

### run.py
Main script that processes the given citation URL or question, verifies the information, and outputs the results.

## Inputs and Outputs

### Inputs
- `citation_url` (optional): URL to the citation to be processed.
- `question` (optional): Direct question to be processed.
- `output_file` (optional): Filename for the output CSV (default: "example_output.csv").

### Outputs
- CSV file containing the decision matrix with statements, citation URLs, decisions, and reasons.
- Prints the fraction of unique statements supported by at least one citation.

## Running the Script

### Prerequisites
- Python 3.x
- Install required libraries: `pandas`, `argparse`, `json`

### Command Line Usage

#### Provide a Citation URL
```bash
python run.py --citation_url "https://my.clevelandclinic.org/health/diseases/8541-thyroid-disease"
```

#### Provide a Question
```bash
python run.py --question "What is the correct dosage for acetaminophen for infants?"
```

# Data

The data are contained in the following Google Drive: [link](https://drive.google.com/drive/folders/1a-i974g3XzLCtZLpTLBbqAwK0olpd5JY?usp=drive_link)
The files are organized as follows:
  - Questions: The 1200 questions used in this analysis. The original documents from Mayo Clinic, UpToDate, and r/AskDocs used to generate each question are not included here due to terms of use for each site. However, the questions generated from each page are available in questions.csv.
  - Responses: The responses for each of the seven models are provided within each CSV in the Responses folder.
  - Parsed Statements: Each response is parsed for medically relevant statements, which are included as a list within a column.
  - Fact-Citation Pairs: The facts are paired with citations provided to back each response.
  - Expert Annotations: The question-annotation pairings from medical experts.
