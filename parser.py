import argparse
from bs4 import BeautifulSoup,NavigableString
import sqlite3
import json
from flask import Flask, render_template
import sqlite3
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_questions')
def get_questions():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, question, answers FROM questions")
    rows = cursor.fetchall()

    questions = [{'id': row[0], 'question': row[1], 'answers': eval(row[2])} for row in rows]

    conn.close()

    return render_template('index.html', questions=questions)
@app.route('/test')
def test():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, question, answers FROM questions")
    rows = cursor.fetchall()

    questions = [{'id': row[0], 'question': row[1], 'answers': eval(row[2])} for row in rows]

    
    question = random.choice(questions)
    print(question['answers'])
    question['correct_answer'] = question['answers'][0]
    answers = random.sample(question['answers'], len(question['answers']))
    correct_answer_count = 0
    for answer in answers:
        if answer == question['correct_answer']:
            question['correct_answer_id'] = correct_answer_count
        correct_answer_count = correct_answer_count+1
    question['answers'] = answers
    conn.close()

    return render_template('test.html', question=question)
    return {'questions': questions}


def store_questions_in_sqlite(data):
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS questions
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       question TEXT,
                       answers TEXT)''')

    # Insert data into the table
    for item in data:
        cursor.execute("INSERT INTO questions (question, answers) VALUES (?, ?)",
                       (item['question'], json.dumps(item['answers'])))

    conn.commit()
    conn.close()

def parse_html(file_name):
    result = []
    with open(file_name, 'r', encoding='utf-8') as file:
        html = file.read()
        question_blocks = html.split('<p class="line"></p>')
        for question_block in question_blocks:
            soup_block = BeautifulSoup(question_block, 'html.parser')
            li_elements = soup_block.find_all('li')
            question = question_block.split('<ol class="elwisOL-lowerLiteral" start="1" type="a">')[0]
            answers = [li.get_text(strip=True) for li in li_elements]
            result.append({"question":question, "answers":answers})
        
        # Find all <hr> tags

    print(result)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process HTML files or serve the application.")
    parser.add_argument('-p', '--parse', action='store_true', help='Parse an HTML file')
    parser.add_argument('-s', '--serve', action='store_true', help='Serve the application')
    parser.add_argument('file_name', nargs='?', help='Name of the HTML file to parse (optional)')
    args = parser.parse_args()

    if args.parse and args.serve:
        parser.error("Cannot parse and serve simultaneously. Please choose one.")

    if args.parse:
        if args.file_name:
            results = parse_html(args.file_name)
            # uncomment in case you want to store questions
            #store_questions_in_sqlite(results)
        else:
            parser.error("Please provide a filename when parsing.")
    elif args.serve:
        app.run(debug=True, host='0.0.0.0', port=8080)
    else:
        parser.print_help()