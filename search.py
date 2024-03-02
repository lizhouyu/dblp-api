import dblp
import json
import argparse

parser = argparse.ArgumentParser()
# the query string, can be assigned with -q or --query
parser.add_argument("-q", "--query", help="query string", type=str, default="machine learning")
# the years list, can be assigned with -y or --years
parser.add_argument("-y", "--years", help="year list", nargs='+', default=["2023"])
# the ccf class list, can be assigned with -c or --ccfs
parser.add_argument("-c", "--ccfs", help="ccf class list", type=list, default=["A"])
args = parser.parse_args()

query = args.query
year_list = args.years
ccf_class_list = args.ccfs

results = dblp.query_for_top_venues(query, year_list, ccf_class_list)

# convert the results to a line-separated string
doc = ''
for result in results:
    doc += 'title: ' + result['title'] + '\n'
    doc += 'authors: ' + ', '.join(result['authors']) + '\n'
    doc += 'venue: ' + result['venue'] + '\n'
    doc += 'year: ' + result['year'] + '\n'
    if result['doi'] is not None:
        doc += 'doi: ' + result['doi'] + '\n'
    if result['url'] is not None:
        doc += 'url: ' + result['url'] + '\n'
    if result['bibtex'] is not None:
        doc += 'bibtex: ' + result['bibtex'] + '\n'
    doc += '\n'

# results file name is query (replace ' ' with '_') + entry in year_list (divided by _) + entry in ccf_class_list (divided by _) 
results_file_name = 'results_' + query.replace(' ', '_') + '_' + '_'.join(year_list) + '_' + '_'.join(ccf_class_list) + '.txt'

# write the results to a text file with the name results_file_name and encoding utf-8
with open(results_file_name, 'w', encoding='utf-8') as f:
    f.write(doc)