package lego.rover.validation

import java.util.ArrayList
import java.util.List
import lego.rover.mission.Action
import lego.rover.mission.Arg
import lego.rover.mission.Args
import lego.rover.mission.Mission
import lego.rover.mission.ActionType

class Auxiliary {	
	def static List<String> ValidArgs(ActionType type) {
		var res = new ArrayList<String>();
		if (type == ActionType.BORDER_ACTION || type == ActionType.COLLISION_ACTION || type == ActionType.ULTRASOUND_ACTION) {
			res.add("rotate_degrees");
		} 
		if (type == ActionType.DRIVE_ACTION) {
			res.add("speed");
		}
		if (type == ActionType.COLOR_DET_ACTION) {
			res.add("colors");
		}
		return res;
	}	
	
	def static boolean EqualUpToRenaming(Mission a, Mission b) {
		if (a.getActions().size() != b.getActions().size()) return false;
		
		for (var i=0; i < a.getActions().size(); i++) {
			if (!EqualAct(a.getActions().get(i), b.getActions().get(i))) return false;
		}
		
		return true;
	}
	
	def static boolean EqualAct(Action x, Action y) {
		if (x.getType() != y.getType()) return false;
		if ((x.getPriority() === null && y.getPriority() !== null) || (x.getPriority() !== null && y.getPriority() === null)) return false;
		if (x.getPriority() !== null && y.getPriority() !== null 
			&& x.getPriority().getPriority() != y.getPriority().getPriority()) return false;
		if (!EqualArgs(x.getArguments(), y.getArguments())) return false;
		
		return true;
	}
	
	def static boolean EqualArgs(Args x, Args y) {
		if (x === null && y === null) return true;
		if (x === null || y === null) return false;
		if (x.getArguments().size() != y.getArguments().size()) return false;
		
		val sortedX = SortArgs(x.getArguments());
		val sortedY = SortArgs(y.getArguments());
		
		for (var i=0; i < x.getArguments().size(); i++)
		{
			if (!sortedX.get(i).x.equals(sortedY.get(i).x) || !sortedX.get(i).y.equals(sortedY.get(i).y)) return false;
		}
		
		return true;
	}
	
	def static List<Tuple> SortArgs(List<Arg> args) {
		var tuples = new ArrayList<Tuple>();
		for (var i=0; i < args.size(); i++) {
			tuples.add(new Tuple(args.get(i).getVar(), args.get(i).getVal()));
		}
		return tuples.sort();
	}	
}