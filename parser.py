import argparse
from bs4 import BeautifulSoup,NavigableString
import sqlite3
import json
from flask import Flask, render_template
import sqlite3

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
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Parse questions and answers from an HTML file.")
    parser.add_argument('file_name', type=str, help='The name of the HTML file to parse.')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call the parsing function with the file name
    results = parse_html(args.file_name)
    #store_questions_in_sqlite(results)
    app.run(debug=True)
