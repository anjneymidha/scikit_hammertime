import requests as re
import pickle as pkl
import json

def scrape_snowmed(df):
    # scan through the dataframe and make a set of all the unique terms
    terms = set()
    for l in df.DRUG:
        for term in l:
            terms.add(term)

    print "total terms: %s" % len(terms)
    # for each term, hit the snomed api
    term_to_drug = {}
    drug_to_ingredient = {}
    ctr = 0
    for term in terms:
        print "on term %s" % ctr
        update_mappings(term, term_to_drug, drug_to_ingredient)
        ctr += 1
    return term_to_drug, None


def update_mappings(term, term_to_drug, drug_to_ingredient):
    # hit the approximate match API to get a rxcui
    r = re.get('http://rxnav.nlm.nih.gov/REST/approximateTerm.json', params={'term':term, 'maxEntries':1})

    js = json.loads(r.text)
    rxcuis = [js['approximateGroup']['candidate'][i]['rxcui'] for i in range(len(js['approximateGroup']['candidate']))]

    # now hit the hierarchy thing to get the chemical ingredients
    for rxcui in rxcuis:
        try:
            ingredient_req = re.get('http://rxnav.nlm.nih.gov/REST/rxcui/%s/hierarchy.json' % rxcui, params={'src':'NDFRT','type':'INGREDIENT'})
            ing_js = json.loads(ingredient_req.text)

    # the first node that is an ingredient type is the collapsed drug name
            for node in ing_js['tree']['node']:
                try:
                  if node['nodeAttr']['attrValue'] == 'INGREDIENT_KIND':
                      drug_name = node['nodeName']
                      term_to_drug[term] = drug_name
                      return
                except:
                    continue
        except:
            continue

if __name__ == '__main__':
#    mapone = {}
#    js = update_mappings('baclofen',mapone,None)
#    df = pkl.load(open('/data/aers/formatted/example_data.df','r'))
    df = pkl.load(open('example_data.df','r'))
    term_to_drug, drug_to_ingredient = scrape_snowmed(df)

