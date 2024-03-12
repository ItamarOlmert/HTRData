import json
import cv2
from pathlib import Path
from utils import *
import io

if __name__ == '__main__':
  dir = Path('.').parent
  idx = 0
  for batch in (dir/"json_files").iterdir():
    with io.open(batch, encoding="utf-8") as file:
      data = json.load(file)
    for image in data['items']:
      annotations = image['annotations']
      words = list(filter(lambda x: x['label_id'] == 0, annotations))
      lines = list(filter(lambda x: x['label_id'] == 1, annotations))
      paragraphs = list(filter(lambda x: x['label_id'] == 2, annotations))
      chars = list(filter(lambda x: x['label_id'] == 3, annotations))
      fpath = dir/"scans"/image['id']
      imgpath = str(fpath/(image['id']+'.jpg'))
      img = cv2.imread(imgpath)
      img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      pars = map(lambda p: Paragraph(p, lines, words, imgpath), paragraphs)
      for i, par in enumerate(pars):
        with io.open(fpath/f'{i}.txt', encoding="utf-8") as text:
          text_words = text.read().split()
        par_words = (word for line in par.children for word in line.children)
        for j, (label, sample) in enumerate(zip(text_words, par_words)):
          name = f"{idx:04d}"
          x, y, w, h = sample.destructure()
          cv2.imwrite(str(dir/"words"/"images"/f'{name}.jpg'), img[round(y):round(y+h), round(x):round(x+w)])
          with io.open(dir/"words"/"labels"/f'{name}.txt', 'w', encoding="utf-8") as f:
            f.write(label)
          idx += 1