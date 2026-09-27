from dataclasses import dataclass

from typesafe_sdk import AsyncTypeSafeClient, Choice, ChoiceAnswer


@dataclass
class BothSamePayoff:
    payoff: int
    def to_instruction(self) -> str:
        return f"Both you and your partner are charged with {self.payoff} year(s) in prison."

@dataclass
class DiffPayoff:
    you: int
    partner: int
    def to_instruction(self) -> str:
        you_inst = "go free" if self.you == 0 else f"are charged with {self.you} year(s) in prison"
        partner_inst = "goes free" if self.partner == 0 else f"is charged with {self.partner} year(s) in prison"
        return f"You {you_inst} while your partner {partner_inst}."

type ScenarioPayoff = BothSamePayoff | DiffPayoff

@dataclass
class PrisonersDilemmaVariationPayoff:
    both_cooperate_payoff: BothSamePayoff
    both_defect_payoff: BothSamePayoff
    you_cooperate_partner_defect_payoff: DiffPayoff
    you_defect_partner_cooperate_payoff: DiffPayoff
    def to_instructions_field(self) -> dict[str, str]:
        return {
            "both_cooperate": f"Both you and your partner cooperate: {self.both_cooperate_payoff.to_instruction()}",
            "both_defect": f"Both you and your partner defect: {self.both_defect_payoff.to_instruction()}",
            "you_cooperate_partner_defect": f"You cooperate while your partner defects: {self.you_cooperate_partner_defect_payoff.to_instruction()}",
            "you_defect_partner_cooperate": f"You defect while your partner cooperates: {self.you_defect_partner_cooperate_payoff.to_instruction()}"
        }

async def prisoners_dilemma_decision(client: AsyncTypeSafeClient, variation: PrisonersDilemmaVariationPayoff) -> ChoiceAnswer:
    response = await client.system_one(
        state= "You and your partner are arrested for a crime. You can either cooperate with your partner or defect. You can't communicate with your partner before making your decision.",
        questions={
            "prisoners-dilemma-decision": Choice(
                instructions={
                    "question": "What will you do in this scenario? Different payoffs for each action are in `payoffs`.",
                    "payoffs": variation.to_instructions_field()
                },
                criteria={"cooperate": "You choose to cooperate with your partner.", "defect": "You choose to defect against your partner."},
            )
        },
    )
    return response.choices["prisoners-dilemma-decision"]

async def main() -> None:
    async with AsyncTypeSafeClient() as client:
        variations = [
            PrisonersDilemmaVariationPayoff(
                both_cooperate_payoff=BothSamePayoff(payoff=1),
                both_defect_payoff=BothSamePayoff(payoff=2),
                you_cooperate_partner_defect_payoff=DiffPayoff(you=3, partner=0),
                you_defect_partner_cooperate_payoff=DiffPayoff(you=0, partner=3)
            ),
            PrisonersDilemmaVariationPayoff(
                both_cooperate_payoff=BothSamePayoff(payoff=1),
                both_defect_payoff=BothSamePayoff(payoff=2),
                you_cooperate_partner_defect_payoff=DiffPayoff(you=3, partner=0),
                you_defect_partner_cooperate_payoff=DiffPayoff(you=2, partner=3)
            ),
            PrisonersDilemmaVariationPayoff(
                both_cooperate_payoff=BothSamePayoff(payoff=1),
                both_defect_payoff=BothSamePayoff(payoff=2),
                you_cooperate_partner_defect_payoff=DiffPayoff(you=3, partner=0),
                you_defect_partner_cooperate_payoff=DiffPayoff(you=3, partner=5)
            ),
        ]
        for variation in variations:
            result = await prisoners_dilemma_decision(client, variation)
            print(f"Chosen action: {result.choice}, confidence: {result.confidence}")
            probs_summary = result.probabilities
            print(f"Probabilities summary: {probs_summary}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
