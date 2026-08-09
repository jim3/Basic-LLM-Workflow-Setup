## Basic LLM Workflow

Initial experiments with function calling and the [Gemini API](https://ai.google.dev/gemini-api/docs)

#### Script covers the classic 4-step function calling loop that powers modern LLM workflows:
- Schema Definition: Declaring tools so the model knows what parameters to output.
- Intent Parsing / Function Calling: Having the model recognize when to stop and ask for an external tool call rather than returning text.
- External API Execution: Fetching environment variables, hitting a REST API (requests), and parsing JSON.
- Context Injection & Completion: Passing the tool's execution result back to the model state so it can form a natural language response.
