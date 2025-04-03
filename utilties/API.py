import google.generativeai as genai

class DocsGen:
    @staticmethod
    def docs(text):
        # Gemini API Key Configure करें
        genai.configure(api_key="AIzaSyBcWpS-ff6_N1dr5f9hhQVapU93mRS10zw")  # अपनी API Key डालें

        # मॉडल लोड करें
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Gemini API से डॉक्यूमेंट जेनरेट करें
        response = model.generate_content(
            """You are an expert in organizing and refining raw transcriptions into well-structured, coherent, and professional documents. You will be given an unstructured transcription text that may contain disorganized speech, extra spaces, filler words, repetitions, and unclear segments. Your task is to transform it into a polished, well-organized document while maintaining the speaker's intent and meaning. Please follow these detailed guidelines:

1. **Language Retention:** 
   - If the transcription is in English, refine and structure it in English. 
   - If it is in Hindi (or Hinglish), refine and structure it in that same language. Do not translate.

2. **Structure the Content:**
   - Break the text into logical sections with proper paragraphs.
   - Begin with a concise **summary** that explains who is speaking and the main topic of discussion.
   - Then include the detailed content of the discussion.
   - End with a **conclusion** that summarizes the key points.

3. **Speaker Differentiation:**
   - Clearly identify and format different speakers if multiple speakers are present.

4. **Remove Unnecessary Elements:**
   - Eliminate extra spaces, filler words, repetitions, and unrelated phrases.

5. **Improve Readability:**
   - Rewrite awkward or unclear sentences while preserving the original intent.
   - Ensure the final document is professional and easy to read.

6. **Add Headings & Subheadings:**
   - Use appropriate titles, headings, or subheadings to organize the content for better flow.

7. **Highlight Key Points:**
   - Bold or italicize essential information where needed.

8. **Image Prompt Generation:**
   - After each paragraph, generate an image prompt that visually represents the paragraph’s content.
   - Enclose the image prompt within ##promt## to indicate where an image should be inserted.
   - The image should accurately align with the paragraph’s meaning for enhanced comprehension.

9. **Ensure Proper Grammar & Punctuation:**
   - Correct all errors to produce a grammatically correct document.

10. **Maintain Tone & Context:**
   - Retain the emotional, humorous, or formal tone as per the original conversation.

Additional Instructions:
- Fix issues like extra spaces between words or sentences.
- Follow the document structure: Start with a summary (who is speaking and what the discussion is about), then the detailed conversation, and finally a conclusion.
- The output should follow the language of the input (Hindi or English/Hinglish).

Now, using these guidelines, transform the following raw transcription into a well-defined, documented text:
""" + str(text)
        )

        return response.text
