from celebrations.basecelebration import BaseCelebration


class DanceCelebration(BaseCelebration):
    def celebrate(self, robot):
        robot.rotate_degrees(2, reverse_before_continue=False, rpm=50)
        robot.rotate_degrees(-4, reverse_before_continue=False, rpm=55)
        robot.rotate_degrees(2, reverse_before_continue=False, rpm=40)
        robot.speak('This makes me sick, let\'s stop')
