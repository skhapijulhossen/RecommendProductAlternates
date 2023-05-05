import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from typing import List, Dict
from fetchProducts import FetchProducts
import pprint
import json

# =======================================================


def FindAlternateGroups(store_domain: str) -> List[Dict]:
    # Get Products
    spider = FetchProducts(store_domain=store_domain)
    df = spider.run()

    # Preprocess the Summary Text
    df['summary'] = df.summary.str.lower()
    df['summary'] = df.summary.str.replace(
        '[^\w\s]', '', regex=True).replace('\d+', '', regex=True)
    df['summary'] = df.summary.str.replace('\d+', '', regex=True)
    vocab_length = len(set(' '.join(df.summary).split(' ')))

    # Extract Summary Text Features
    vectorizer = TfidfVectorizer(
        lowercase=False, max_features=vocab_length, stop_words='english')
    features = vectorizer.fit_transform(df.summary).toarray()

    # Reduce the Dimensionality
    pca = PCA(n_components=10)
    features_2_dim = pca.fit_transform(features)

    # Cluster Groups
    groups = df.product_type.value_counts().shape[0]
    grouper = KMeans(n_clusters=groups)
    df['group'] = grouper.fit_predict(features_2_dim)

    # Get Alternate Groups
    product_alternates = []
    for grp in set(grouper.labels_):
        alternatives = df.loc[df.group == grp, 'link'].to_list()
        product_alternates.append({"product alternates": alternatives})

    # Save Alternate Groups
    # filename = store_domain.split('.')[1]
    # with open(f'alternates/{filename}.json', mode='w') as file:
    #     json.dump(product_alternates, file, indent=4)

    return product_alternates


if __name__ == '__main__':
    recom = FindAlternateGroups(
        store_domain='https://www.boysnextdoor-apparel.co')
    recom = FindAlternateGroups(
        store_domain='https://www.woolsboutiqueuomo.com')
    recom = FindAlternateGroups(
        store_domain='https://sartale2022.myshopify.com')
    # recom = FindAlternateGroups(store_domain='https://berkehome.pl')
    # recom = FindAlternateGroups(store_domain='https://glamaroustitijewels.com')
    # recom = FindAlternateGroups(store_domain='https://lampsdepot.com')
    # recom = FindAlternateGroups(store_domain='https://kitchenoasis.com')
