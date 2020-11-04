package gameoflife.generator

import java.util.List
import gameoflife.gol.Rule
import gameoflife.gol.OnOff
import java.util.ArrayList

class Auxiliary {
	def static List<Rule> filterRules(List<Rule> rules, OnOff filterBy) {	
		var List<Rule> res = new ArrayList<Rule>();
		for (Rule r : rules) {
			if (r.onOff == filterBy) res.add(r);
		}
		return res;
	}
}