from typesafe_sdk import AsyncTypeSafeClient, Choice


async def jev_fizz_buzz(n: int, client: AsyncTypeSafeClient) -> str:
    response = await client.system_one(
        state=f"The number {n} is the input to the FizzBuzz problem.",
        questions={
            "fizz-buzz-output": Choice(
                instructions="What is the FizzBuzz output for the given number? Fizz if divisible by 3, Buzz if divisible by 5, FizzBuzz if divisible by both, none otherwise.",
                criteria={"fizz": None, "buzz": None, "fizzbuzz": None, "none": None},
            )
        },
    )
    return response.choices["fizz-buzz-output"].choice

def regular_fizz_buzz(n: int) -> str:
    if n % 3 == 0 and n % 5 == 0:
        return "fizzbuzz"
    elif n % 3 == 0:
        return "fizz"
    elif n % 5 == 0:
        return "buzz"
    else:
        return "none"

async def main() -> None:
    async with AsyncTypeSafeClient() as client:
        for n in range(1, 101):
            result = await jev_fizz_buzz(n, client)
            regular_result = regular_fizz_buzz(n)
            match = "❌" if result != regular_result else "✅"
            print(f"Number {n}: JEV={result}, Regular={regular_result} {match}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
