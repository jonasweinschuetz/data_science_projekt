import re



def regex_filter(regex, l):
    return [entry for entry in l if re.search(regex, entry)]

# 
def apply_regexs(regexs, l):
    r = []
    for regex in regexs:
        r += regex_filter(regex,l)
    return r

# takes list of search terms (or 2-tuples of search terms) and return regex that checks if term is contained somewhere
def generate_regex(search_terms):
    r = []
    for term in search_terms:
        if isinstance(term, tuple):
            term1, term2 = term
            r.append(f".*{term1}.*{term2}.*")
            r.append(f".*{term2}.*{term1}.*")
        else:
            r.append(f".*{term}.*")
    return r
