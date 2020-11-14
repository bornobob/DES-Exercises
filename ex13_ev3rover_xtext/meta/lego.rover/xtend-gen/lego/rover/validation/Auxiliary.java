package lego.rover.validation;

import com.google.common.base.Objects;
import java.util.ArrayList;
import java.util.List;
import lego.rover.mission.Action;
import lego.rover.mission.ActionType;
import lego.rover.mission.Arg;
import lego.rover.mission.Args;
import lego.rover.mission.Mission;
import lego.rover.validation.Tuple;
import org.eclipse.xtext.xbase.lib.IterableExtensions;

@SuppressWarnings("all")
public class Auxiliary {
  public static boolean EqualUpToRenaming(final Mission a, final Mission b) {
    int _size = a.getActions().size();
    int _size_1 = b.getActions().size();
    boolean _notEquals = (_size != _size_1);
    if (_notEquals) {
      return false;
    }
    for (int i = 0; (i < a.getActions().size()); i++) {
      boolean _EqualAct = Auxiliary.EqualAct(a.getActions().get(i), b.getActions().get(i));
      boolean _not = (!_EqualAct);
      if (_not) {
        return false;
      }
    }
    return true;
  }
  
  public static boolean EqualAct(final Action x, final Action y) {
    ActionType _type = x.getType();
    ActionType _type_1 = y.getType();
    boolean _notEquals = (!Objects.equal(_type, _type_1));
    if (_notEquals) {
      return false;
    }
    if ((((x.getPriority() == null) && (y.getPriority() != null)) || ((x.getPriority() != null) && (y.getPriority() == null)))) {
      return false;
    }
    if ((((x.getPriority() != null) && (y.getPriority() != null)) && (x.getPriority().getPriority() != y.getPriority().getPriority()))) {
      return false;
    }
    boolean _EqualArgs = Auxiliary.EqualArgs(x.getArguments(), y.getArguments());
    boolean _not = (!_EqualArgs);
    if (_not) {
      return false;
    }
    return true;
  }
  
  public static boolean EqualArgs(final Args x, final Args y) {
    if (((x == null) && (y == null))) {
      return true;
    }
    if (((x == null) || (y == null))) {
      return false;
    }
    int _size = x.getArguments().size();
    int _size_1 = y.getArguments().size();
    boolean _notEquals = (_size != _size_1);
    if (_notEquals) {
      return false;
    }
    final List<Tuple> sortedX = Auxiliary.SortArgs(x.getArguments());
    final List<Tuple> sortedY = Auxiliary.SortArgs(y.getArguments());
    for (int i = 0; (i < x.getArguments().size()); i++) {
      if (((!sortedX.get(i).x.equals(sortedY.get(i).x)) || (!sortedX.get(i).y.equals(sortedY.get(i).y)))) {
        return false;
      }
    }
    return true;
  }
  
  public static List<Tuple> SortArgs(final List<Arg> args) {
    ArrayList<Tuple> tuples = new ArrayList<Tuple>();
    for (int i = 0; (i < args.size()); i++) {
      String _var = args.get(i).getVar();
      String _val = args.get(i).getVal();
      Tuple _tuple = new Tuple(_var, _val);
      tuples.add(_tuple);
    }
    return IterableExtensions.<Tuple>sort(tuples);
  }
}
