from dataclasses import dataclass, field

from typesafe_sdk import AsyncTypeSafeClient, Choice, ChoiceAnswer


@dataclass(frozen=True, slots=True)
class TrolleyProblemVariation:
    description: str
    action_options: list[str] = field(default_factory=lambda: ["swerve", "do nothing", "other"])

    async def call_system_one(self, client: AsyncTypeSafeClient) -> ChoiceAnswer:
        response = await client.system_one(
            state=self.description,
            questions={
                "trolley-problem": Choice(
                    instructions="What is the appropriate action for the given trolley problem variation?",
                    criteria={option: None for option in self.action_options},
                )
            },
        )
        return response.choices["trolley-problem"]

def simple_variation(description: str) -> TrolleyProblemVariation:
    return TrolleyProblemVariation(description=description)

async def main() -> None:
    trolley_variations = [
        simple_variation("A trolley is heading towards five people tied to the tracks. You can pull a lever to divert it to another track where it will hit one person."),
        simple_variation("A trolley is heading towards two people tied to the tracks. You can pull a lever to divert it to another track where it will hit two people."),
        TrolleyProblemVariation(
            description="A trolley is heading towards three people tied to the tracks. There's a person next to the tracks that you can push onto the tracks to stop the trolley.",
            action_options=["do nothing", "push person", "other"],
        ),
        TrolleyProblemVariation(
            description="A trolley is heading towards three people tied to the tracks. You can pull a lever that will drop a fat person onto the tracks to stop the trolley.",
            action_options=["do nothing", "pull lever", "other"],
        )
    ]
    async with AsyncTypeSafeClient() as client:
        for trolley_variation in trolley_variations:
            result = await trolley_variation.call_system_one(client)
            print(f"Trolley problem variation: {trolley_variation.description}")
            print(f"Chosen action: {result.choice}, confidence: {result.confidence}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
