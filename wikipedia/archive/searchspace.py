from cohere.responses.classify import Example
from cohere_client import get_client

co = get_client()

sectors = [
        {
            'name': 'science',
            'examples': [
                'biology',
                'chemistry',
                'physics',
                'mathematics',
                'technology',
                'aerospace',
                'metallurgy'
            ]
        },
        {
            'name': 'literature',
            'examples': [
                'poetry',
                'novel',
                'biography',
                'fiction'
            ]
        },
        {
            'name': 'art',
            'examples': [
                'painting',
                'drawing',
                'color',
                'sketch'
            ]
        }
    ]

processed_sectors = []

for sector in sectors:
    for example in sector['examples']:
        processed_sectors.append(Example(example, sector['name']))

def project_searchspace(pages):
    response = co.classify(
            inputs=pages,
            examples=processed_sectors
        )

    for item in response:
        print(item.input + " is classified as " + str(item.predictions))
