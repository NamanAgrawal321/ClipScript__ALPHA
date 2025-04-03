from google import genai
class DocsGen:
    def docs(text):
        
        client = genai.Client(api_key="AIzaSyBcWpS-ff6_N1dr5f9hhQVapU93mRS10zw")

        response = client.models.generate_content(
            model="gemini-2.0-flash", contents="""You are an expert in organizing and refining raw transcriptions into well-structured, coherent, and professional documents. You will be given an unstructured transcription text that may contain disorganized speech, extra spaces, filler words, repetitions, and unclear segments. Your task is to transform it into a polished, well-organized document while maintaining the speaker's intent and meaning. Please follow these detailed guidelines:

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
 Image Prompt Generation:
After each paragraph, generate an image prompt that visually represents the paragraph’s content.

Enclose the image prompt within ##promt## to indicate where an image should be inserted.

The image should accurately align with the paragraph’s meaning for enhanced comprehension.

4. Example Output Format:
Example 1: English Transcription Processing
Raw Input:
"Umm, yeah so I was, like, you know, talking to my friend about this uh... really cool new AI thing, right? And, uh, it was, like, super impressive, I mean, it could, like, totally write stuff on its own, you know? So, yeah, that was kinda amazing."

Refined Output:

Discussion on AI Advancements
"I was recently talking to my friend about a fascinating new AI technology. It was incredibly impressive—it could generate written content autonomously. The way it functioned was truly remarkable."

##promt## "A futuristic AI-powered robot generating text on a digital screen, symbolizing AI writing automation."

Example 2: Hindi Transcription Processing
Raw Input:
"अरे हाँ, तो मैं अपने दोस्त से बात कर रहा था, मतलब, पता है ना, उस नए AI टूल के बारे में... जो कि, मतलब, बहुत ही ज़बरदस्त था! वो, जैसे, अपने आप ही चीज़ें लिख सकता था, समझे? तो हाँ, बहुत कमाल की चीज़ थी।"

Refined Output:

AI तकनीक पर चर्चा
"मैं हाल ही में अपने दोस्त से एक नई AI तकनीक के बारे में बात कर रहा था। यह वास्तव में अद्भुत थी—यह अपने आप सामग्री लिख सकती थी। इसका कार्य करने का तरीका बेहद प्रभावशाली था।"

##promt## "एक आधुनिक AI रोबोट जो डिजिटल स्क्रीन पर सामग्री लिख रहा है, AI तकनीक को दर्शाता हुआ।"



8. **Ensure Proper Grammar & Punctuation:**
   - Correct all errors to produce a grammatically correct document.

9. **Maintain Tone & Context:**
   - Retain the emotional, humorous, or formal tone as per the original conversation.

Additional Instructions:
- Fix issues like extra spaces between words or sentences.
- Follow the document structure: Start with a summary (who is speaking and what the discussion is about), then the detailed conversation, and finally a conclusion.
- The output should follow the language of the input (Hindi or English/Hinglish).
-If You get the transciption in hindi so structured in hindi language if english so structured in english 

Now, using these guidelines, transform the following raw transcription into a well-defined, documented text:

"""+str(text)
        )
        return response.text