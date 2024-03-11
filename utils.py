import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

colors = ['red', 'green', 'purple', 'blue']

class BoundingBox:
    def __init__(self, annotation, path):
      self.x, self.y, self.w, self.h = annotation['bbox']
      self.children = []
      self.color = "yellow"
      self.path = path

    def plot(self, ax):
      ax.add_patch(Rectangle((self.x, self.y), self.w, self.h, linewidth=.5, edgecolor=self.color, facecolor='none'))
      for c in self.children:
        c.plot(ax)

    def destructure(self):
      return self.x, self.y, self.w, self.h

    def contains(self, x, y, w, h):
      center_x = x + w / 2
      center_y = y + h / 2
      corner_x = self.x + self.w
      corner_y = self.y + self.h
      return self.x < center_x < corner_x and self.y < center_y < corner_y

    def plot_all(self):
      image = plt.imread(self.path)
      fig, ax = plt.subplots(dpi=300)
      ax.imshow(image)
      self.plot(ax)
      fig.show()

class Character(BoundingBox):
    def __init__(self, annotation, path):
      super().__init__(annotation)
      self.color = colors[3]

class Word(BoundingBox):
    def __init__(self, annotation, path):
      super().__init__(annotation, path)
      self.color = colors[0]

class Line(BoundingBox):
    def __init__(self, annotation, words, path):
      super().__init__(annotation, path)
      self.color = colors[1]
      for word in words:
        if self.contains(*word['bbox']):
          self.children.append(Word(word, path))
      self.children.sort(key = lambda word: word.x, reverse=True)

class Paragraph(BoundingBox):
    def __init__(self, annotation, lines, words, path):
      super().__init__(annotation, path)
      self.color = colors[2]
      for line in lines:
        if self.contains(*line['bbox']):
          self.children.append(Line(line, words, path))
      self.children.sort(key = lambda line: line.y)

def plot_bbs(annotations, path="Form #1A.jpg"):
  image = plt.imread(path)
  fig, ax = plt.subplots(dpi=300)
  ax.imshow(image)
  for annotation in annotations:
    x, y, w, h = annotation['bbox']
    ax.add_patch(Rectangle((x, y), w, h, linewidth=.5, edgecolor=colors[annotation['label_id']], facecolor='none'))
  fig.show()