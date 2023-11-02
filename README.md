# Web3 Governance Summariser
This project is a work-in-progress. The ultimate intention is to create an LLM agent that can ingest, summarise and explain, governance proposals of Web3 DAOs.

So far it is just a simple summariser of Governance proposals using OpenAI.

## Usage

Install the necessary packages:

```bash
$ poetry install
```

Add your OpenAI API key to a `.env` file in the root directory:

```.env
OPENAI_API_KEY="<your-api-key>"
```

Run the summariser by providing the URL of a Governance proposal submission:

```bash
poetry run python src/proposal_summary.py "https://www.comp.xyz/t/cgp-2-0-updates-and-renewal/4518"
```

The result should look something like this:

```
Proposal Summary:
The text describes the updates and renewal of the Compound Grants Program (CGP) 2.0. The program has been running successfully for two quarters, and after receiving feedback from the community and builders, the proposal is to renew it with a budget of $970,000 spread across three domains. The text also includes background information on the progress of CGP 2.0, metrics on its performance, insights and feedback, challenges, expected improvements, and compensation for committee members. The proposal includes specifications, implementation details, funding breakdowns, and KPIs and expectations for the renewed program. Finally, the text mentions the involvement of Questbook, a decentralized grant orchestration tool, and provides next steps for community feedback and voting on the proposal.

Discussion Summary:
Overall, the sentiment expressed in the discussion forums is overwhelmingly positive and appreciative of the Compound Grants Program (CGP) 2.0. Grantees express gratitude for the support they received and highlight the straightforward application process, quick feedback, and efficient approval process. There is also emphasis on the transparency, accountability, and efficiency of the program. Participants in the program express satisfaction with their experience and express support for renewing the grant program. Some suggestions for improvement include providing incentives for quality feedback, creating more venues for discussions, and conducting surveys among grantees for feedback. Overall, there is a strong sentiment of appreciation and support for the CGP 2.0 and its renewal.``

```

## Contribution

This project is not looking for contributions until it is in a more stable state.
