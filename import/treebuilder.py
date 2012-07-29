from HTMLParser import HTMLParser




class Tag:
  def __init__(self, name, attrs):
    self.Name = name
    self.Attributes = attrs
    self.Contents = []
  
  def out(self, indent = 0):
    ind = indent * " "
    print ind, self.Name
    for i in self.Contents:
      try:
        i.out(indent + 2)
      except:
        print ind, "  ", i

  def gobble_text(self):
    results = []
    for i in self.Contents:
      try:
        results.append(i.gobble_text())
      except:
        results.append(i)
    return " ".join(results)
  
  def first_text(self):
    for i in self.Contents:
      if isinstance(i, str):
        return i
    raise RuntimeError, "no first text. sorry."

  def get_all(self, name):
    def matches(tag):
      try:
        return tag.Name == name
      except:
        return False

    return filter(matches, self.Contents)

  def count(self, name):
    return len(self.get_all(name))

  def __getitem__(self, (key, number)):
    return self.get_all(key)[number]




class TreeBuilderParser(HTMLParser):
    IGNORING = 0
    PROCESSING = 1
    DONE = 2

    SINGLE_TAGS = [ "img", "br" ]

    def __init__(self):
        HTMLParser.__init__(self)
        self.Mode = self.PROCESSING
        self.DocumentRoot = Tag("document-root", {})
        self.ElementStack = [ self.DocumentRoot ]

    def handle_comment(self, data):
        pass

    def handle_starttag(self, tag_name, attrs):
        if self.Mode == self.PROCESSING:
            tag = Tag(tag_name, attrs)
            self.ElementStack[0].Contents.append(tag)
            if tag_name not in self.SINGLE_TAGS:
                self.ElementStack.insert(0, tag)
    def handle_data(self, data):
        if self.Mode == self.PROCESSING:
            s = data.strip()
            if len(s):
                self.ElementStack[0].Contents.append(s)

    def handle_endtag(self, tag):
        if self.Mode == self.PROCESSING:
            closed_el = self.ElementStack.pop(0)
            if len(self.ElementStack) == 0:
                self.Mode = self.DONE
                return
            if closed_el.Name != tag:
                raise RuntimeError, "closing wrong tag. expected %s, got %s at %s." % (
                    self.ElementStack[0].Name, tag, self.getpos())

    def root(self):
        return self.DocumentRoot
