FORMAT_SEARCH_RESULTS = """\
{% for result in search_results %}
<search_result>
{{ result }}
</search_result>
{% endfor %}"""
