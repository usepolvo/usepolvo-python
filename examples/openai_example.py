import asyncio

from usepolvo.tentacles.openai import OpenAIClient
from usepolvo.tentacles.openai.completions.schemas import CompletionRequest

client = OpenAIClient()


async def create_completion():
    request = CompletionRequest(
        prompt="Translate the following English text to Spanish: 'Hello, how are you?'", max_tokens=50
    )
    response = await client.completions.create(request.model_dump())
    print(f"Completion: {response['choices'][0]['text']}")


async def main():
    # Create a completion
    await create_completion()

    # You could add more OpenAI-specific operations here

    # Keep the script running (for demonstration purposes)
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
