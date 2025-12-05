import os
import typer
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich.prompt import Prompt
from pathlib import Path
import re

app = typer.Typer()
console = Console()

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

def parse_html(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")

    questions = []
    
    # Find all question blocks
    # Based on the HTML provided, questions are in <azt-question-standalone-for-student-at-review-page>
    question_blocks = soup.find_all("azt-question-standalone-for-student-at-review-page")
    
    skipped_count = 0
    skeleton_count = 0

    for block in track(question_blocks, description=f"Parsing {file_path.name}..."):
        try:
            # Check for skeleton/loading block
            if block.find("div", class_="skeleton-box-loading"):
                skeleton_count += 1
                continue

            # Extract Question Text
            q_content_box = block.find("azt-question-content-box")
            if not q_content_box:
                skipped_count += 1
                continue
            
            q_text_elem = q_content_box.find("azt-dynamic-hook")
            q_text = q_text_elem.get_text(strip=True) if q_text_elem else ""
            
            # Extract Options
            options = []
            answer_box = block.find("azt-question-answer-view-content-box")
            if answer_box:
                option_divs = answer_box.find_all("div", class_="answer")
                for opt in option_divs:
                    label_elem = opt.find("b", class_="answer-label")
                    content_elem = opt.find("azt-dynamic-hook")
                    
                    label = label_elem.get_text(strip=True).replace(".", "") if label_elem else ""
                    content = content_elem.get_text(strip=True) if content_elem else ""
                    options.append(f"{label}. {content}")
            
            # Extract Correct Answer
            correct_answer = ""
            user_answer_box = block.find("azt-answer-box-with-user-full-answer-for-student")
            if user_answer_box:
                key_text = user_answer_box.find("span", class_="keyText")
                if key_text:
                    # Format is usually "Đáp án đúng: A"
                    match = re.search(r"Đáp án đúng:\s*([A-D])", key_text.get_text(strip=True))
                    if match:
                        correct_char = match.group(1)
                        # Find the full text for this option
                        for opt in options:
                            if opt.startswith(f"{correct_char}."):
                                correct_answer = opt
                                break
                        if not correct_answer:
                             correct_answer = f"Option {correct_char}"

            if q_text and options and correct_answer:
                questions.append({
                    "question": q_text,
                    "options": options,
                    "answer": correct_answer
                })
            else:
                skipped_count += 1
        except Exception as e:
            console.print(f"[red]Error parsing a question block: {e}[/red]")

    if skeleton_count > 0:
        console.print(f"[yellow]Warning: {skeleton_count} questions were skipped because they were not fully loaded (skeleton blocks).[/yellow]")
        console.print("[yellow]Tip: Scroll to the bottom of the page to load all questions before saving the HTML.[/yellow]")
    if skipped_count > 0:
        console.print(f"[yellow]Warning: {skipped_count} questions were skipped due to missing content or parsing errors.[/yellow]")

    return questions

def save_to_anki(questions, output_path: Path):
    with open(output_path, "w", encoding="utf-8") as f:
        for q in questions:
            # Front: Question + Options
            front = f"{q['question']}<br><br>" + "<br>".join(q['options'])
            # Back: Correct Answer
            back = q['answer']
            
            # Escape semicolons if necessary (simple replacement for now)
            front = front.replace(";", ",")
            back = back.replace(";", ",")
            
            f.write(f"{front};{back}\n")

@app.command()
def main():
    if not INPUT_DIR.exists():
        console.print(f"[red]Input directory '{INPUT_DIR}' not found![/red]")
        return

    html_files = list(INPUT_DIR.glob("*.html"))
    if not html_files:
        console.print(f"[yellow]No HTML files found in '{INPUT_DIR}'[/yellow]")
        return

    console.print("[bold green]Found HTML files:[/bold green]")
    for idx, file in enumerate(html_files):
        console.print(f"{idx + 1}. {file.name}")

    choice = Prompt.ask("Select a file number to process (or 'all')", default="all")

    files_to_process = []
    if choice.lower() == "all":
        files_to_process = html_files
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(html_files):
                files_to_process = [html_files[idx]]
            else:
                console.print("[red]Invalid selection[/red]")
                return
        except ValueError:
            console.print("[red]Invalid input[/red]")
            return

    OUTPUT_DIR.mkdir(exist_ok=True)

    for file in files_to_process:
        console.print(f"\n[bold]Processing {file.name}...[/bold]")
        questions = parse_html(file)
        
        if questions:
            output_file = OUTPUT_DIR / f"{file.stem}.csv"
            save_to_anki(questions, output_file)
            console.print(f"[green]Saved {len(questions)} flashcards to {output_file}[/green]")
        else:
            console.print(f"[yellow]No questions found in {file.name}[/yellow]")

if __name__ == "__main__":
    app()
