📘 Adobe Hackathon 2025 – Round 1A Submission
🧠 Project: Multilingual Heading Detection and Outline Extraction from PDFs

📌 Problem Statement
Given an academic or research PDF, extract the document title and a clean outline of the document (including headings with their hierarchical levels and page numbers) in a structured JSON format, completely offline and within strict runtime and size constraints.

💡 Our Approach
To solve this challenging task effectively and efficiently, we designed a hybrid system combining rule-based heuristics and a lightweight multilingual ML classifier. Here's how the system works:

🧠 1. Font-Based Layout Analysis
We analyzed fonts by:
- Size: Larger font size typically implies heading.
- Boldness: Detected from font names and weight.
- Color: Text color deviations often indicate headers.
- Frequency: The most frequent font size is usually body text.

📄 2. Candidate Extraction from PDFs
Using PyMuPDF, we extract merged spans of text blocks with font metadata. Filters exclude:
- Headers/footers
- Mathematical blocks (symbols like ∀, ∑, ⊆, etc.)
- Captions and noisy blocks

🤖 3. Machine Learning Classifier (Multilingual)
A lightweight Logistic Regression classifier was trained with:
- Features: font_size, is_bold, x, y, char_length, body_font_size
- Model size: ~2 KB
- Languages tested: English, Hindi, Chinese, Japanese, German, Spanish, Russian

🔄 4. Final Pipeline
PDF → Candidate Extractor → ML Heading Classifier → Level Estimation → Output JSON

🚀 Performance & Constraints
- Inference Time (50-page PDF): 8–9 seconds ✅
- Internet Access: ❌ Not Required ✅
- Docker Image Size: ~724MB ✅
- CPU-Only: ✅ Compatible
- JSON Output Format: ✅ Valid
- Multilingual PDFs: ✅ Tested

🗂 Directory Structure
- Dockerfile
- requirements.txt
- README.md
- outline_extractor.py
- extract_candidates.py
- utils.py
- model/heading_model.pkl
- input/
- output/

🔧 Build & Run (Offline Dockerized)
Build:
docker build --platform linux/amd64 -t adobe-phase1final:latest .

Run:
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none adobe-phase1final:latest

📤 Output Format
{
  "title": "Machine Learning Foundations",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "Supervised Learning", "page": 3 },
    { "level": "H3", "text": "Decision Trees", "page": 4 }
  ]
}

🧠 Model Details
- Model: Logistic Regression
- Features: Font features + layout
- Accuracy: ~85%
- Size: ~2 KB
- Languages: 7+ tested

🧪 PDF Types Tested
- Research papers
- Textbooks
- Literature
- Scientific books
- Multilingual and noisy PDFs

🛠 Requirements (in Docker)
- python==3.10
- PyMuPDF==1.23.12
- scikit-learn==1.4.1.post1
- joblib==1.4.2

🙋 Author
Team NoName
Jitendra Kumar, Team Leader, Email: jitendra0905kumar@gmail.com
Yousha Raza
GitHub: github.com/yourusername

✅ Final Notes
- Offline inference
- Sub-10s runtime
- Small model size
- Language-agnostic
