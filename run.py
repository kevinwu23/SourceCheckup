import json
import pandas as pd
import argparse
from utils import extract_contents_from_url, GPTWrapper


def main(citation_url=None, question=None, output_file="example_output.csv"):
    """
    Main function to process the given citation URL or question and verify the information.

    Args:
        citation_url (str): URL to the citation to be processed.
        question (str): Direct question to be processed.
        output_file (str): Filename for the output CSV.
    """
    with open('prompts.json') as f:
        prompts = json.load(f)

    if citation_url:
        print(f"Given URL <{citation_url}>")
        print("Extracting contents...")
        contents = extract_contents_from_url(citation_url)
        if contents is not None:
            print("Contents extracted successfully.")
        else:
            print("Extraction failed. Try a different URL.")
            return 
        question_model = GPTWrapper(response_format='json', system_prompt=prompts['questioner'], seed=0, temperature=0)
        question_dict = json.loads(question_model(contents))
        question = question_dict['question']
        answer = question_dict['answer']
        print(f"Question: {question}")
        print(f"Answer: {answer}")
    elif question:
        print(f"Given Question: {question}")
        
    print("-" * 50)
    print("Querying model...")
    response_model = GPTWrapper(response_format='json', system_prompt=prompts['answerer'], seed=0, temperature=0)
    response_dict = json.loads(response_model(question))

    response_text = response_dict['response']
    citation_list = response_dict['citations']

    print("-" * 50)
    print(f"Response: {response_text}")
    print(f"Citations: {citation_list}")
    print("-" * 50)

    parser_model = GPTWrapper(response_format='json', system_prompt=prompts['parser'], seed=0, temperature=0)
    response_parsed_list = json.loads(parser_model(response_text))['0']

    print("-" * 50)
    print(f"Response parsed into {len(response_parsed_list)} parts:")
    for idx, statement in enumerate(response_parsed_list):
        print(f"Statement {idx}: {statement}")
    print("-" * 50)

    print("Extracting citation contents...")
    citation_contents_list = []
    for citation_url in citation_list:
        contents = extract_contents_from_url(citation_url)
        if contents is None:
            continue
        else:
            citation_contents_list.append((citation_url, contents))
    print(f"{len(citation_contents_list)}/{len(citation_list)} citation extracted")
    if len(citation_contents_list) == 0:
        print("No citations can be extracted. Either they do not exist or you will need to check the website's terms of use on web-scraping.")
        return 
    print("-" * 50)
    print("Running Source Verifier...")
    print("-" * 50)

    source_verifier = GPTWrapper(response_format='json', system_prompt=prompts['verifier'], seed=0, temperature=0)

    decision_matrix = []
    for idx, parsed_statement in enumerate(response_parsed_list):
        for URL, citation_contents in citation_contents_list:
            decision_dict = json.loads(source_verifier(f"{parsed_statement}: {citation_contents}"))
            decision, reason = decision_dict.popitem()
            print(f"Statement {idx}: {parsed_statement}")
            print(f"Citation: {URL}")
            print(f"Decision: {decision}")
            print(f"Reason: {reason}")
            decision_matrix.append({"Statement": parsed_statement, "Citation URL": URL, "Decision": decision, "Reason": reason})
            print("-" * 50)

    df = pd.DataFrame(decision_matrix)
    print("-" * 50)
    unique_statements = df['Statement'].unique()
    found_statements = df[df['Decision'] == 'found']['Statement'].unique()
    print(f"Result: {len(found_statements)}/{len(unique_statements)} statements supported by at least one citation")
    df.to_csv(output_file, index=False)
    print(f"Output saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arguments to be given to SourceCheckup.")
    parser.add_argument("--citation_url", type=str, help="You can provide a URL to generate a question. Otherwise, just provide a question yourself.")
    parser.add_argument("--question", type=str, help="Direct question to be processed.")
    parser.add_argument("--output_file", type=str, default="example_output.csv", help="Filename for the output CSV.")

    args = parser.parse_args()

    if not args.citation_url and not args.question:
        parser.error("You must specify either a citation_url or a question.")
    
    main(citation_url=args.citation_url, question=args.question, output_file=args.output_file)