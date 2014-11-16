import requests as re
import lxml


def hit_api(drug_name, src, tp):
    '''
    hits snomed's class hierarchy api by first finding the drugs rxcui and then hitting the hierarcy api with params src=src and type=tp
    '''

    # first, get the drug's rxcui
    r = re.get('http://rxnav.nlm.nih.gov/REST/rxcui', params={'name':drug_name})

    # parse the xml to find the id
    rxcui = get_rxcui_from_tree(r.text)

    # hit the class hierarchy endpoint
    hierarcy= re.get('http://rxnav.nlm.nih.gov/REST/rxcui/%s/hierarchy' % rxcui, params={'src':src, 'type':tp})





def get_rxcui_from_tree(xml):
    # make tree
    tree = ET.ElementTree(ET.fromstring(xml))

    for x in tree.iter():
        if x.tag == 'rxnormId':
            return int(x.text)

    # traverse down children until we find the element called "rxnormID"_
