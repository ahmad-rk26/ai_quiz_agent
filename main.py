# import os
# from extract_text import extract_text
# from generate_mcqs import generate_mcqs
# from create_html import create_html

# def main():
#     file_path = input("Enter the path to your media file (e.g., sample.pdf): ").strip('"')

#     # Auto detect file type
#     ext = os.path.splitext(file_path)[1].lower()
#     ext_map = {
#         ".pdf": "pdf",
#         ".docx": "docx",
#         ".jpg": "image",
#         ".jpeg": "image",
#         ".png": "image",
#         ".bmp": "image",
#         ".txt": "txt"      # NEW
#     }

#     if ext not in ext_map:
#         print(f"Unsupported file format: {ext}")
#         print("Supported: pdf, docx, image formats, txt")
#         return

#     file_type = ext_map[ext]
#     print(f"Detected file type: {file_type.upper()}")

#     num_questions = int(input("How many MCQs to generate? (e.g., 5): "))

#     print("Extracting text...")
#     text = extract_text(file_path, file_type)

#     if not text or "Error" in text:
#         print(text or "Error: Could not extract text.")
#         return

#     print(f"Extracted text (first 500 chars): {text[:500]}...")

#     print("Generating MCQs...")
#     mcqs = generate_mcqs(text, num_questions)
#     if "error" in mcqs[0]:
#         print(mcqs[0]["error"])
#         return

#     print(f"Generated {len(mcqs)} MCQs.")

#     print("Creating quiz HTML...")
#     create_html(mcqs)
#     print("Done! Open 'quiz.html' in your browser to take the quiz.")

# if __name__ == "__main__":
#     main()
