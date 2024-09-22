from bs4 import BeautifulSoup
import re
import sys

def parse_questions_and_answers(html_content):
    print(123)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    questions_and_answers = []
    print(123)
    # Find all question-answer pairs
    for p in soup.find_all('p'):
        if p.text.strip().isdigit():  # This is likely a question number
            question_text = p.next_sibling.text.strip()
            
            ol = p.next_sibling.next_sibling
            
            if ol and ol.name == 'ol' and ol.get('class') == ['elwisOL-lowerLiteral']:
                answers = [li.text.strip() for li in ol.find_all('li')]
                
                # Remove empty lines and extra spaces
                answers = [re.sub(r'\s+', ' ', answer).strip() for answer in answers]
                
                questions_and_answers.append({
                    'question': question_text,
                    'answers': answers,
                    'correct_answer': answers[0]  # Always option A
                })
    
    return questions_and_answers

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py input_file.html")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        print(123)
        with open(filename, 'r', encoding='utf-8-sig') as file:
            html_content = file.read()
        
        print(123)
        parsed_data = parse_questions_and_answers(html_content)

        for item in parsed_data:
            print(f"Question: {item['question']}")
            print("Answers:")
            for i, answer in enumerate(item['answers'], 1):
                print(f"{chr(64 + i)}) {answer}")
            print(f"Correct Answer: {item['correct_answer']}\n")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
