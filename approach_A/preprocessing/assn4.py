from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd


# Specify the DBPedia endpoint
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")


# Query for the description of "Capsaicin", filtered by language
sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?comment
    WHERE { <http://dbpedia.org/resource/Capsaicin> rdfs:comment ?comment
    FILTER (LANG(?comment)='en')
    }
""")

# Convert results to JSON format
sparql.setReturnFormat(JSON)
result = sparql.query().convert()

# The return data contains "bindings" (a list of dictionaries)
for hit in result["results"]["bindings"]:
    # We want the "value" attribute of the "comment" field
    print(hit["comment"]["value"])

results_df = pd.io.json.json_normalize(results['results']['bindings'])
results_df[['item.value', 'itemLabel.value']]