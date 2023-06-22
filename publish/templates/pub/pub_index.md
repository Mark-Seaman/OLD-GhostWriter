{% autoescape off %}# {{ title }}


{% for doc in docs %}* {{ doc }}
{% endfor %} 
{% endautoescape %}