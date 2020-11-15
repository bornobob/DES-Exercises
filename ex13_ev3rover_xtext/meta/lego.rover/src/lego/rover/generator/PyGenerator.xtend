package lego.rover.generator

import java.util.List
import lego.rover.mission.Action
import lego.rover.mission.Mission
import lego.rover.mission.Priority
import lego.rover.mission.Simulation
import lego.rover.mission.Args
import lego.rover.mission.Arg

class PyGenerator {
	def static ToText(Simulation simulation)'''
		from actions import *
		from runner import Runner
		from robot import Robot
		«"\n\n"»
		def create_runner():
			r = Robot()
			«FOR m : simulation.missions.missions SEPARATOR "\n"»«MissionToText(m)»«ENDFOR»
			Runner(r, mission_«simulation.robots.robots.get(0).mission»).run()
		«"\n\n"»
		if __name__ == '__main__':
			create_runner()
	'''
	
	def static MissionToText(Mission m)'''«IF (m.actions === null || m.actions.size() == 0)»mission_«m.name» = []«ELSE»mission_«m.name» = «ActionsToText(m.actions)»«ENDIF»'''
	
	def static ActionsToText(List<Action> acts)'''[«FOR i : 0 ..< acts.size() SEPARATOR ", "»«ActionToText(acts.get(i), i)»«ENDFOR»]'''
	
	def static ActionToText(Action action, int default_prio)'''«action.type.toString()»(priority=«PriorityToText(action.priority, default_prio)»«ArgsToText(action.arguments)»)'''
	
	def static ArgsToText(Args args)'''«IF (args !== null && args.arguments.size() > 0)», «FOR a : args.arguments SEPARATOR ", "»«ArgToText(a)»«ENDFOR»«ENDIF»'''
	
	def static ArgToText(Arg arg)'''«arg.^var»=«arg.^val»'''
	
	def static PriorityToText(Priority priority, int default_prio)'''«IF (priority === null)»«default_prio»«ELSE»«priority.priority»«ENDIF»'''
}
