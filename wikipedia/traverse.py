import wikipedia

def search(startPage, endPage):
  currentPage = wikipedia.page(startPage, redirect=True)
  priorNodes = {}
  queue = queue_heuristic(endPage)
  queue.addlist(currentPage.links)
  currentPage = currentPage.title

  visited = set()

  while(currentPage != endPage):
    print("looking at page " + currentPage)
    visited.add(currentPage)
    # extremely questionable
    try:
      nextPage = wikipedia.page(currentPage)
      for page in nextPage.links:
        if not page in visited:
          priorNodes[page] = nextPage.title
          visited.add(page)
          # print(nextPage.title + " -> " + page)
      queue.addlist(nextPage.links)
    except:
      # print("We got an error, but we are skipping it")
      pass
    currentPage = queue.pop()

  # print("calls: " + str(queue.calls))

  # print(priorNodes)

  path = []

  while True:
    try:
      path.append(currentPage)
      currentPage = priorNodes[currentPage]
    except:
      break
  
  path.reverse()

  return path

search("Southwest Mountains", "Mountain")
