package gameoflife.generator

import gameoflife.gol.TotalRules
import java.util.List
import gameoflife.gol.Rule
import gameoflife.gol.OnOff
import gameoflife.gol.Operator
import gameoflife.gol.ElseRule
import gameoflife.gol.OnOffCurrent

class PyGenerator {
	def static ToText(TotalRules root)'''
		def apply_rules(current_value, total, on_value, off_value):
			«rules2Text(root.onRules, OnOff.ON)»
			«rules2Text(root.offRules, OnOff.OFF)»
			«elseRule2Text(root.elseRule)»
	'''
	
	def static CharSequence rules2Text(List<Rule> rules, OnOff onOff)'''
		«IF (rules.size > 0)»
			if current_value == «onOff2Text(onOff)»:
			«if2Text(rules, OnOff.ON)»
			«if2Text(rules, OnOff.OFF)»
		«ENDIF»
	'''
	
	def static CharSequence if2Text(List<Rule> rules, OnOff onOff)'''
		«IF (!Auxiliary.filterRules(rules, onOff).isEmpty())» 
			«"\t"»if «FOR r : Auxiliary.filterRules(rules, onOff) SEPARATOR " or "»current_value «operator2Text(r.op)» «r.compareValue»«ENDFOR»:
			«"\t\t"»return «onOff2Text(onOff)»
		«ENDIF»
	'''
	
	def static CharSequence elseRule2Text(ElseRule elseRule)'''
		«IF (elseRule === null)»
		return current_value
		«ELSE»
		return «onOffCur2Text(elseRule.onOffCur)»
		«ENDIF»
	'''
	
	def static CharSequence onOffCur2Text(OnOffCurrent value) {
		switch (value){
			case OnOffCurrent::ON: return '''on_value'''
			case OnOffCurrent::OFF: return '''off_value'''
			case OnOffCurrent::CURRENT: return '''current_value'''
		}	
	}
	
	def static CharSequence onOff2Text(OnOff value) {
		switch (value){
			case OnOff::ON: return '''on_value'''
			case OnOff::OFF: return '''off_value'''
		}	
	}
	
	def static CharSequence operator2Text(Operator operator) {
		switch (operator){
			case Operator::LT: return '''<'''
			case Operator::GT: return '''>'''
			case Operator::EQ: return '''=='''
			case Operator::GEQ: return '''>='''
			case Operator::LEQ: return '''<='''
		}	
	}
}