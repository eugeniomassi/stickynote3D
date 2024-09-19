class PostIt:
    def __init__(self, title, description, user, datetime, location, color=(1.0, 1.0, 0.0), size=1.0):
        self.title = title
        self.description = description
        self.user = user
        self.datetime = datetime.now().strftime("%H:%M %d/%m/%Y")
        self.location = location
        self.color = color
        self.size = size

# Array globale di Post-it
post_its = []
