import asyncio

from usepolvo.tentacles.openai import OpenAIClient
from usepolvo.tentacles.openai.completions.schemas import CompletionRequest

client = OpenAIClient()


def create_completion():
    request = CompletionRequest(
        messages=[
            {"role": "system", "content": "Translate the following English text to Spanish: 'Hello, how are you?'"}
        ]
    )
    response = client.completions.create(request.model_dump(exclude_none=True))
    print(f"Completion: {response.choices[0].message.content}")


async def main():
    # Create a completion
    create_completion()

    # You could add more OpenAI-specific operations here

    # Keep the script running (for demonstration purposes)
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
