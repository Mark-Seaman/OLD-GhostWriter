# Seaman's Log Weekly 

{{ day }}


{% for doc in docs %}* {{ doc.date }} - [{{ doc.title }}]({{ doc.url }})
{% endfor %}
