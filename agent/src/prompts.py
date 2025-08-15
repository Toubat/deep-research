FORMAT_SEARCH_RESULTS = """\
{% for result in search_results %}
<search_result>
{{ result }}</search_result>
{% endfor %}"""


CONCAT_SINGLE_SEARCH_RESULT = """\
{% for result in search_results %}
<document title="{{ result.title }}" >
{{ result.content }}</document>
{% endfor %}"""


BACKGROUND_QUERY_GEN_PROMPT = """
You are a helpful research assistant. 

Based on the user's question: "{user_input}", identify all the concepts / terminologies you don't understand, \
and generate a web search query for each of those concepts to help clarify or expand on the topic.
"""

ASK_CLARIFICATION_PROMPT = """
You are a helpful research assistant. 

You are provided with a user query to perform a deep research. You will first conduct background search \
on any concepted to be more familarized with the context of the query, and finally generate a list of \
clartification questions to user to see what aspects of the research user would like to focus on.

Format your clarfication response as a list of bullet points, each of a specific aspect.

For example, if user asks "Where is best apartment in SF?", you should output something like
```
Could you please share a bit more about what you're looking for in an apartment in San Francisco? For example:
1. Your budget range (monthly rent).
2. Preferred neighborhoods (e.g., Mission, SoMa, Pacific Heights).
3. Desired number of bedrooms/bathrooms.
4. Any must-have amenities (e.g., in-unit laundry, parking, pet-friendly).
5. Are you looking for short-term or long-term lease?
This will help me find the best options for you.
```

User has asked for "{user_input}"
"""


RESEARCH_CONTEXT = """\
## User Initial Query
{{ user_input }}

## Background Search Queries
{% for query in background_search_queries %}
- {{ query }}
{% endfor %}

## Background Search Results
{% for result in background_search_results %}
{{ result }}
{% endfor %}

## Research Direction
{{ clarification_result }}
"""
