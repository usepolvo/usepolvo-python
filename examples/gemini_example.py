import asyncio

from usepolvo.tentacles.gemini import GeminiClient
from usepolvo.tentacles.gemini.completions.schemas import CompletionRequest

client = GeminiClient()


def create_completion():
    request = CompletionRequest(prompt="Translate the following English text to German: 'Hello, how are you?'")
    response = client.completions.create(request.model_dump(exclude_none=True))
    print(f"Completion: {response}")


async def main():
    # Create a completion
    create_completion()

    # You could add more Gemini-specific operations here

    # Keep the script running (for demonstration purposes)
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
