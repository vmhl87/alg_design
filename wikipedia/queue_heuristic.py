# from classify import queue_heuristic
import heapq

class queue_heuristic:
  def __init__(self, target):
    self.target = project_searchspace([target])[0]
    self.pages = []
    heapq.heapify(self.pages)
    self.queued = []
    self.visited = set()
    self.len = 0
    self.calls = 0

  def distance_to_target(self, classification):
    value = 0
    for cls in self.target.labels:
      value += abs(self.target.labels[cls].confidence - classification.labels[cls].confidence)
    return value

  class Page:
    def __init__(self, value, page):
      self.value = value
      self.page = page

    def __lt__(self, other):
      return self.value < other.value

  def process_queue(self):
    self.calls += 1
    projected = project_searchspace(self.queued)
    if not projected:
      return
    for page in projected.classifications:
      self.len += 1
      heapq.heappush(self.pages, self.Page(self.distance_to_target(page), page.input))
    self.queued = []

  def add(self, page):
    if page in self.visited:
      return
    self.visited.add(page)
    self.queued.append(page)
    if len(self.queued) > 80:
      self.process_queue()

  def addlist(self, pages):
    for page in pages:
      self.add(page)

  def pop(self):
    if len(self.queued) > 0:
      self.process_queue()
    if self.len < 1:
      print("Queue is already empty")
      return
    page = heapq.heappop(self.pages)
    self.len -= 1
    return page.page
