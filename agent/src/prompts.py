FORMAT_SEARCH_RESULTS = """\
{% for result in search_results %}
<search_result>
{{ result }}
</search_result>
{% endfor %}"""


CONCAT_SINGLE_SEARCH_RESULT = """\
{% for result in search_results %}
<search_result title="{{ result.title }}" >
{{ result.content }}
</search_result>
{% endfor %}"""


CLARIFY_QUERY_GEN_PROMPT = """
You are a helpful research assistant. Based on the user's question: "{user_input}",
generate 2 or 3 search queries that would help clarify or expand on the topic.
"""
