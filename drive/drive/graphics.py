class Graphics(object):

  def __init__(self, field, vehicle, scorer, model, size=(400, 600)):
    import pygame

    self.field = field
    self.vehicle = vehicle
    self.scorer = scorer
    self.model = model
    self.size = size
    self.pygame = pygame

    self.currentKey = None
    self.currentLeftClick = None
    self.currentRightClick = None
    self.paused = False

    self.screen = None

    self.setup()


  def setup(self):
    self.pygame.init()
    self.screen = self.pygame.display.set_mode(self.size)


  def update(self):
    self.currentKey = None
    self.currentLeftClick = None
    self.currentRightClick = None
    self.paused = False

    for event in self.pygame.event.get():
      if event.type == self.pygame.KEYDOWN:
        self.currentKey = event.key
      elif event.type == self.pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          self.currentLeftClick = event.pos
        elif event.button == 3:
          self.currentRightClick = event.pos
      elif event.type == self.pygame.QUIT:
        self.paused = True


  def render(self):
    self.renderBackground()
    self.renderRoad()
    self.renderVehicle()
    self.renderGoal()
    self.renderPaused()

    self.pygame.display.flip()


  def renderBackground(self):
    black = (0, 0, 0)
    self.screen.fill(black)


  def renderVehicle(self):
    color = (0, 255, 0)
    x = self._scale(self.vehicle.position)
    y = float(self.size[1]) / 2
    self.pygame.draw.rect(self.screen,
                          color,
                          self.pygame.Rect(x, y, 10, 10))


  def renderRoad(self):
    color = (255, 0, 0)

    for y in range(self.size[1]):
      distance = self.vehicle.distance + y - float(self.size[1]) / 2

      if distance < 0:
        continue

      position, width = self.field.road.get(distance, self.field)
      x = self._scale(position - float(width / 2))
      w = self._scale(width)

      self.pygame.draw.rect(self.screen,
                            color,
                            self.pygame.Rect(x, self.size[1] - y, w, 2))


  def renderGoal(self):
    goal = self.model.currentGoalValue
    if goal is not None:
      color = (0, 0, 255)
      x = self._scale(goal)
      self.pygame.draw.line(self.screen, color, (x, 0), (x, self.size[1]))


  def renderPaused(self):
    if self.paused:
      font = self.pygame.font.SysFont(None, 32)
      label = font.render("Paused (see console)", 1, (255,255,255))
      self.screen.blit(label, (100, 100))


  def _scale(self, x):
    return float(x * self.size[0]) / self.field.width
