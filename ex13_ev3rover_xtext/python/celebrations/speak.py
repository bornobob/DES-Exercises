from celebrations.basecelebration import BaseCelebration


class SpeakCelebration(BaseCelebration):
    def __init__(self, speaketh):
        self.speaketh = speaketh

    def celebrate(self, robot):
        robot.speak(self.speaketh)
