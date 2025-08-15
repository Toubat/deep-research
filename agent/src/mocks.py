MOCK_SEARCH_QUERIES = [
    "MCP acronym meaning and common contexts",
    "A2A acronym definition and typical uses",
]

MOCK_SEARCH_RESULT = [
    """<document title="MCP - Definition by AcronymFinder" >
MCP - Definition by AcronymFinder What does MCP stand for? Link/Page Citation "Click to see Link/Page Citation info") MLA style: "MCP." Acronym Finder. | MCP | Master Control Program |  | | MCP | Message Control Program |  | | MCP | Master Computer Program |  | | MCP | More Coffee Please |  | | MCP | Maintenance Computer Program |  | | MCP | Myrinet Control Program |  | | MCP | Management Control Program |  | | MCP | Master Control Processor |  | | MCP | Mission City Press |  | | MCP | Maintenance Control Program |  | Note: We have 250 other definitions for MCP in our Acronym Attic MCP+I MCP-1 MCP-CE MCP-D MCP/AS MCP/PMT MCP1 MCP3</document>

<document title="A Comprehensive Guide to Understanding MCP (Model Context ..." >
Therefore, MCP means: Model Context Protocol. It is a standardized set of rules agreed upon (by developers) to define the conversational context for interacting</document>

<document title="Model Context Protocol - Wikipedia" >
The **Model Context Protocol** (**MCP**) is an open standard, open-sourceframework introduced by Anthropic in November 2024 to standardize the way artificial intelligence (AI) systems like large language models (LLMs) integrate and share data with external tools, systems, and data sources. The protocol was announced by Anthropic in November 2024 as an open standard for connecting AI assistants to data systems such as content repositories, business management tools, and development environments. Demis Hassabis, CEO of Google DeepMind, confirmed in April 2025 MCP support in the upcoming Gemini "Gemini (chatbot)") models and related infrastructure, describing the protocol as "rapidly becoming an open standard for the AI agentic era". "Introducing Model Context Protocol (MCP) in Copilot Studio: Simplified Integration with AI Apps and Agents".</document>

<document title="Introducing the Model Context Protocol - Anthropic" >
*   Claude Today, we're open-sourcing the Model Context Protocol (MCP), a new standard for connecting AI assistants to the systems where data lives, including content repositories, business tools, and development environments. The Model Context Protocol is an open standard that enables developers to build secure, two-way connections between their data sources and AI-powered tools. Claude 3.5 Sonnet is adept at quickly building MCP server implementations, making it easy for organizations and individuals to rapidly connect their most important datasets with a range of AI-powered tools. All Claude.ai plans support connecting MCP servers to the Claude Desktop app. Claude for Work customers can begin testing MCP servers locally, connecting Claude to internal systems and datasets.</document>

<document title="MCP Explained: A simple guide for product teams" >
We’ll explore some of the high level technical concepts involved in MCP, why it matters to product teams along with some real world examples from leading companies like Block and Microsoft. Plus, practical ways MCP can be used during the product development process with tools like Figma and Jira. * How you can use MCP during the product development process for testing and integrating Figma and Jira into engineering tools MCP helps the model connect to the tools or resources that provide that context that it needs and the protocol makes this easier for engineers. The MCP Protocol gives developers a standardised way for product teams to connect their AI assistants with external things like databases, tools, APIs and any other resource that might be useful.</document>""",
    """
<document title="A2A Military Abbreviation Meaning - All Acronyms" >
A2A Military Abbreviation. A2A in Military commonly refers to Air-To-Air, which describes a type of combat or engagement between aircraft.</document>

<document title="A2A - Definition by AcronymFinder" >
What does A2A stand for? ; A2A, Alpha-2 Adrenergic (receptor) ; A2A, Access to Archives (UK) ; A2A · Air-To-Air (weapon) ; A2A, Athens-to-Atlanta (in-line skating</document>

<document title="What does A2A mean? Why do people use jargon that others don't ..." >
A2A means “Asked to Answer” and you should never use it (if you're the one who is writing the answer). Sometimes, you know the question and a</document>

<document title="How to understand the difference between API, MCP, and A2A in ..." >
As AI takes center stage in translation workflows, you’re no longer just dealing with CAT tools, TMSs, and connectors—you have to deal with two more acronyms: MCP and A2A. This post explains the difference between API, MCP (Model Context Protocol), and A2A (Agent-to-Agent Protocol)—and how each fits into the future of AI-powered localization. Even when calling AI models (like GPT or a machine translation engine), your TMS or connector uses an API. While client libraries can make tool descriptions more convenient, and you still need to execute the tools when the model requests them, MCP provides a consistent framework that works across different AI systems. These agentic interoperability tools create opportunities for Translation AI Agents to serve every department, from customer support to legal, providing consistent, policy-compliant translations throughout the organization.</document>

<document title="A2A, MCP, and ADK — Clarifying Their Roles in the AI Ecosystem" >
A2A, in contrast, is all about agent-to-agent communication. It defines how agents discover each other, negotiate tasks, exchange messages, and</document>""",
]

MOCK_CLARIFICATION_QUESTION = """
Could you help me narrow down what you mean by “MCP” and “A2A”? For example:  
1. For MCP:  
   • Are you asking about a financial metric (e.g., Margin Control Profitability)?  
   • An AI/LLM integration standard (Model Context Protocol)?  
   • Some other industry or technology acronym?  
2. For A2A:  
   • Account-to-Account payments or banking transactions?  
   • Agent-to-Agent collaboration in enterprise automation?  
   • “Ask to Answer” jargon used on platforms like Quora?  
   • Or another domain entirely?  
3. Which industry or application are you focused on (e.g., finance, AI development, marketing)?  
4. How deep a dive do you need? (High-level definitions vs. technical details and examples)  
5. Any particular use case or project context you have in mind?
"""

MOCK_CLARIFICATION_RESULT = """
test result
"""


MOCK_STATE_PATCH = dict(
    background_search_queries=MOCK_SEARCH_QUERIES,
    background_search_results=MOCK_SEARCH_RESULT,
    background_messages=[],
    clarification_question=MOCK_CLARIFICATION_QUESTION,
    clarification_result=MOCK_CLARIFICATION_RESULT,
    report_sections=[],
    research_results={},
)
