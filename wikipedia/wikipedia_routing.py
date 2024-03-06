import wikipedia

def adj(page):
    try:
        response = wikipedia.page(page)

        return response.links
    except:
        return []
