import time

from google import genai

from config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPT


class GeminiBrain:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def ask(self, prompt):

        full_prompt = f"""
{SYSTEM_PROMPT}

User:
{prompt}
"""

        max_attempts = 4

        for attempt in range(max_attempts):

            try:

                print(
                    f"Gemini attempt {attempt + 1}/{max_attempts}..."
                )

                response = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=full_prompt,
                )

                answer = (response.text or "").strip()

                if not answer:
                    return "I didn't get a response from Gemini."

                return answer

            except Exception as error:

                error_text = str(error)

                print(
                    f"Gemini attempt {attempt + 1} failed:"
                )
                print(error_text)

                # Retry only temporary server/rate-limit errors
                if "503" in error_text or "429" in error_text:

                    if attempt < max_attempts - 1:

                        wait_time = 2 ** attempt

                        print(
                            f"Retrying in {wait_time} seconds..."
                        )

                        time.sleep(wait_time)

                    else:

                        raise

                else:

                    raise