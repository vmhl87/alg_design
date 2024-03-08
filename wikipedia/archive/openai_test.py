from openai import OpenAI
client = OpenAI()

def gpt_encode(word):
    response = client.embeddings.create(input=[word], model='text-embedding-ada-002')
    return response['data'][0].embedding
