# Ramesh Project

A Python-based project implementing asynchronous research and data processing capabilities.

## Features

- Asynchronous search operations
- Parallel task execution
- AI-driven data synthesis
- Structured output generation

## Requirements

- Python 3.8+
- praisonaiagents
- duckduckgo_search
- pydantic
- asyncio

## Installation

1. Clone the repository:
```bash
git clone https://github.com/FarhanAkhtar121/ramesh.git
cd ramesh
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main application:
```bash
python app.py
```

The application will:
1. Execute parallel search tasks
2. Process and synthesize the results
3. Generate a structured output file

## Project Structure

- `app.py`: Main application file containing the async implementation
- `requirements.txt`: Project dependencies
- `research.md`: Output file for research results

## Output

Results are saved to `/tmp/research.md` in JSON format.