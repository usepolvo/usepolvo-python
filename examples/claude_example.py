import asyncio

from usepolvo.tentacles.claude import ClaudeClient
from usepolvo.tentacles.claude.completions.schemas import CompletionRequest

client = ClaudeClient()


async def create_completion():
    request = CompletionRequest(
        prompt="Translate the following English text to French: 'Hello, how are you?'", max_tokens_to_sample=100
    )
    response = await client.completions.create(request.model_dump())
    print(f"Completion: {response['completion']}")


async def main():
    # Create a completion
    await create_completion()

    # You could add more Claude-specific operations here

    # Keep the script running (for demonstration purposes)
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
