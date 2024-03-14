import wikipedia

def search(startPage, endPage):
  currentPage = wikipedia.page(startPage, redirect=True)
  priorNodes = {}
  queue = queue_heuristic(endPage)
  queue.addlist(currentPage.links)
  currentPage = currentPage.title

  while(currentPage != endPage):
    print("looking at page " + currentPage)
    best = queue.pop()
    # extremely questionable
    try:
      nextPage = wikipedia.page(best)
      priorNodes[nextPage.title] = currentPage
      queue.addlist(nextPage.links)
      currentPage = nextPage.title
    except:
      # print("We got an error, but we are skipping it")
      pass

  # print("calls: " + str(queue.calls))

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
