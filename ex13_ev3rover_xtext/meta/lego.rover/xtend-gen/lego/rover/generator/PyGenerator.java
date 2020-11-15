package lego.rover.generator;

import java.util.List;
import lego.rover.mission.Action;
import lego.rover.mission.Arg;
import lego.rover.mission.Args;
import lego.rover.mission.Mission;
import lego.rover.mission.Priority;
import lego.rover.mission.Simulation;
import org.eclipse.emf.common.util.EList;
import org.eclipse.xtend2.lib.StringConcatenation;
import org.eclipse.xtext.xbase.lib.ExclusiveRange;

@SuppressWarnings("all")
public class PyGenerator {
  public static CharSequence ToText(final Simulation simulation) {
    StringConcatenation _builder = new StringConcatenation();
    _builder.append("from actions import *");
    _builder.newLine();
    _builder.append("from runner import Runner");
    _builder.newLine();
    _builder.append("from robot import Robot");
    _builder.newLine();
    _builder.append("\n\n");
    _builder.newLineIfNotEmpty();
    _builder.append("def create_runner():");
    _builder.newLine();
    _builder.append("\t");
    _builder.append("r = Robot()");
    _builder.newLine();
    _builder.append("\t");
    {
      EList<Mission> _missions = simulation.getMissions().getMissions();
      boolean _hasElements = false;
      for(final Mission m : _missions) {
        if (!_hasElements) {
          _hasElements = true;
        } else {
          _builder.appendImmediate("\n", "\t");
        }
        CharSequence _MissionToText = PyGenerator.MissionToText(m);
        _builder.append(_MissionToText, "\t");
      }
    }
    _builder.newLineIfNotEmpty();
    _builder.append("\t");
    _builder.append("Runner(r, mission_");
    String _mission = simulation.getRobots().getRobots().get(0).getMission();
    _builder.append(_mission, "\t");
    _builder.append(").run()");
    _builder.newLineIfNotEmpty();
    _builder.append("\n\n");
    _builder.newLineIfNotEmpty();
    _builder.append("if __name__ == \'__main__\':");
    _builder.newLine();
    _builder.append("\t");
    _builder.append("create_runner()");
    _builder.newLine();
    return _builder;
  }
  
  public static CharSequence MissionToText(final Mission m) {
    StringConcatenation _builder = new StringConcatenation();
    {
      if (((m.getActions() == null) || (m.getActions().size() == 0))) {
        _builder.append("mission_");
        String _name = m.getName();
        _builder.append(_name);
        _builder.append(" = []");
      } else {
        _builder.append("mission_");
        String _name_1 = m.getName();
        _builder.append(_name_1);
        _builder.append(" = ");
        CharSequence _ActionsToText = PyGenerator.ActionsToText(m.getActions());
        _builder.append(_ActionsToText);
      }
    }
    return _builder;
  }
  
  public static CharSequence ActionsToText(final List<Action> acts) {
    StringConcatenation _builder = new StringConcatenation();
    _builder.append("[");
    {
      int _size = acts.size();
      ExclusiveRange _doubleDotLessThan = new ExclusiveRange(0, _size, true);
      boolean _hasElements = false;
      for(final Integer i : _doubleDotLessThan) {
        if (!_hasElements) {
          _hasElements = true;
        } else {
          _builder.appendImmediate(", ", "");
        }
        CharSequence _ActionToText = PyGenerator.ActionToText(acts.get((i).intValue()), (i).intValue());
        _builder.append(_ActionToText);
      }
    }
    _builder.append("]");
    return _builder;
  }
  
  public static CharSequence ActionToText(final Action action, final int default_prio) {
    StringConcatenation _builder = new StringConcatenation();
    String _string = action.getType().toString();
    _builder.append(_string);
    _builder.append("(priority=");
    CharSequence _PriorityToText = PyGenerator.PriorityToText(action.getPriority(), default_prio);
    _builder.append(_PriorityToText);
    CharSequence _ArgsToText = PyGenerator.ArgsToText(action.getArguments());
    _builder.append(_ArgsToText);
    _builder.append(")");
    return _builder;
  }
  
  public static CharSequence ArgsToText(final Args args) {
    StringConcatenation _builder = new StringConcatenation();
    {
      if (((args != null) && (args.getArguments().size() > 0))) {
        _builder.append(", ");
        {
          EList<Arg> _arguments = args.getArguments();
          boolean _hasElements = false;
          for(final Arg a : _arguments) {
            if (!_hasElements) {
              _hasElements = true;
            } else {
              _builder.appendImmediate(", ", "");
            }
            CharSequence _ArgToText = PyGenerator.ArgToText(a);
            _builder.append(_ArgToText);
          }
        }
      }
    }
    return _builder;
  }
  
  public static CharSequence ArgToText(final Arg arg) {
    StringConcatenation _builder = new StringConcatenation();
    String _var = arg.getVar();
    _builder.append(_var);
    _builder.append("=");
    String _val = arg.getVal();
    _builder.append(_val);
    return _builder;
  }
  
  public static CharSequence PriorityToText(final Priority priority, final int default_prio) {
    StringConcatenation _builder = new StringConcatenation();
    {
      if ((priority == null)) {
        _builder.append(default_prio);
      } else {
        int _priority = priority.getPriority();
        _builder.append(_priority);
      }
    }
    return _builder;
  }
}
