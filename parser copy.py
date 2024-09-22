import argparse
from bs4 import BeautifulSoup

def parse_html(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find all questions
    questions = soup.find_all('p')

    # Find all answers (ordered lists)
    answers = soup.find_all('ol')

    parsed_data = []

    # Iterat e through questions and answers and store them
    for question, answer in zip(questions, answers):
        question_text = question.text.strip()
        answer_choices = answer.find_all('li')
        choices = [choice.text.strip() for choice in answer_choices]

        parsed_data.append({
            'question': question_text,
            'answers': choices
        })

    # Output parsed data
    for item in parsed_data:
        print(f"Question: {item['question']}")
        for i, answer in enumerate(item['answers'], 1):
            print(f"  {chr(96 + i)}. {answer}")
        print("\n")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Parse questions and answers from an HTML file.")
    parser.add_argument('file_name', type=str, help='The name of the HTML file to parse.')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the parsing function with the file name
    parse_html(args.file_name)
