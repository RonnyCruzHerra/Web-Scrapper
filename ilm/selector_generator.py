import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_version = os.getenv("AZURE_OPENAI_VERSION")

client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version=api_version,
)

def generar_selector(html: str, objetivo: str) -> str:
    prompt = f"""
    Dado el siguiente HTML, genera un selector CSS o XPath que seleccione el elemento que contiene: "{objetivo}".
    HTML:
    {html}
    """
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "Eres un experto en scraping web."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Error llamando a AzureOpenAI: {e}")
