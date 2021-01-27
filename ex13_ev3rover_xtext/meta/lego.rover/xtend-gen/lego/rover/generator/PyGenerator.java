package lego.rover.generator;

import com.google.common.base.Objects;
import java.util.List;
import lego.rover.mission.Action;
import lego.rover.mission.ActionType;
import lego.rover.mission.BorderAction;
import lego.rover.mission.Celebration;
import lego.rover.mission.CollisionAction;
import lego.rover.mission.Color;
import lego.rover.mission.ColorDetAction;
import lego.rover.mission.DanceCelebration;
import lego.rover.mission.DontDrownAction;
import lego.rover.mission.DriveAction;
import lego.rover.mission.MeasureAction;
import lego.rover.mission.Mission;
import lego.rover.mission.Missions;
import lego.rover.mission.Priority;
import lego.rover.mission.PushRockAction;
import lego.rover.mission.Rotation;
import lego.rover.mission.SpeakCelebration;
import lego.rover.mission.Speed;
import lego.rover.mission.UltrasoundAction;
import org.eclipse.emf.common.util.EList;
import org.eclipse.xtend2.lib.StringConcatenation;
import org.eclipse.xtext.xbase.lib.ExclusiveRange;

@SuppressWarnings("all")
public class PyGenerator {
  public static CharSequence SlaveToText() {
    StringConcatenation _builder = new StringConcatenation();
    _builder.append("from runner import Runner");
    _builder.newLine();
    _builder.append("from robot import Robot");
    _builder.newLine();
    _builder.append("from ev3dev2.sensor.lego import UltrasonicSensor, TouchSensor");
    _builder.newLine();
    _builder.append("from utils import SensorMap, BluetoothSlave");
    _builder.newLine();
    _builder.append("from actions import DataAction");
    _builder.newLine();
    _builder.append("from mission import Mission");
    _builder.newLine();
    _builder.append("\n\n");
    _builder.newLineIfNotEmpty();
    _builder.append("MAC_ADDRESS = \'00:1a:7d:da:71:10\'  # Mac address via which the Robots connect with bluetooth");
    _builder.newLine();
    _builder.append("PORT = 4  # Port on which the Robots connect with bluetooth");
    _builder.newLine();
    _builder.append("\n");
    _builder.newLineIfNotEmpty();
    _builder.append("sensor_map_slave = {\'ts_b\': TouchSensor(\'ev3-ports:in1\'), \'ts_l\': TouchSensor(\'ev3-ports:in2\'),");
    _builder.newLine();
    _builder.append("                    ");
    _builder.append("\'ts_r\': TouchSensor(\'ev3-ports:in3\'), \'us_f\': UltrasonicSensor(\'ev3-ports:in4\')}");
    _builder.newLine();
    _builder.append("\n");
    _builder.newLineIfNotEmpty();
    _builder.append("def create_runner():");
    _builder.newLine();
    _builder.append("\t");
    _builder.append("r = Robot(SensorMap(sensor_map_slave), bluetooth=BluetoothSlave(MAC_ADDRESS, PORT))");
    _builder.newLine();
    _builder.append("\t");
    _builder.append("Runner(r, [Mission([DataAction(1, polling_rate=250)])]).run()");
    _builder.newLine();
    _builder.append("\n\n");
    _builder.newLineIfNotEmpty();
    _builder.append("if __name__ == \'__main__\':");
    _builder.newLine();
    _builder.append("\t");
    _builder.append("create_runner()");
    _builder.newLine();
    return _builder;
  }
  
  public static CharSequence MainToText() {
    StringConcatenation _builder = new StringConcatenation();
    _builder.append("import subprocess");
    _builder.newLine();
    _builder.append("import time");
    _builder.newLine();
    _builder.append("\n\n");
    _builder.newLineIfNotEmpty();
    _builder.append("PYTHON_EXECUTABLE = \'python\'");
    _builder.newLine();
    _builder.append("BRICK_1_PY = \'main_main.py\'");
    _builder.newLine();
    _builder.append("BRICK_2_PY = \'main_slave.py\'");
    _builder.newLine();
    _builder.append("\n\n");
    _builder.newLineIfNotEmpty();
    _builder.append("if __name__ == \"__main__\":");
    _builder.newLine();
    _builder.append("    ");
    _builder.append("proc1 = subprocess.Popen([PYTHON_EXECUTABLE, BRICK_1_PY])");
    _builder.newLine();
    _builder.append("    ");
    _builder.append("time.sleep(1)");
    _builder.newLine();
    _builder.append("    ");
    _builder.append("proc2 = subprocess.Popen([PYTHON_EXECUTABLE, BRICK_2_PY])");
    _builder.newLine();
    _builder.append("\n");
    _builder.newLineIfNotEmpty();
    _builder.append("    ");
    _builder.append("input(\'Press [enter] to stop the simulation\')");
    _builder.newLine();
    _builder.append("    ");
    _builder.append("proc2.kill()");
    _builder.newLine();
    _builder.append("    ");
    _builder.append("proc1.kill()");
    _builder.newLine();
    return _builder;
  }
  
  public static CharSequence ToText(final Missions simulation) {
    StringConcatenation _builder = new StringConcatenation();
    _builder.append("from actions.measureaction import MeasureAction");
    _builder.newLine();
    _builder.append("from actions import *");
    _builder.newLine();
    _builder.append("from runner import Runner");
    _builder.newLine();
    _builder.append("from ev3dev2.unit import STUD_MM");
    _builder.newLine();
    _builder.append("from robot import Robot");
    _builder.newLine();
    _builder.append("from ev3dev2.sensor.lego import UltrasonicSensor, ColorSensor");
    _builder.newLine();
    _builder.append("from ev3dev2.wheel import EV3EducationSetTire");
    _builder.newLine();
    _builder.append("from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_D, MoveDifferential, Motor");
    _builder.newLine();
    _builder.append("from utils import SensorMap, BluetoothMaster");
    _builder.newLine();
    _builder.append("from celebrations import *");
    _builder.newLine();
    _builder.append("from mission import Mission");
    _builder.newLine();
    _builder.append("\n\n");
    _builder.newLineIfNotEmpty();
    _builder.append("MAC_ADDRESS = \'00:1a:7d:da:71:10\'  # Mac address via which the Robots connect with bluetooth");
    _builder.newLine();
    _builder.append("PORT = 4  # Port on which the Robots connect with bluetooth");
    _builder.newLine();
    _builder.append("\n");
    _builder.newLineIfNotEmpty();
    _builder.append("sensor_map_master = {\'tank_drive\': MoveDifferential(OUTPUT_A, OUTPUT_D, EV3EducationSetTire, 15 * STUD_MM),");
    _builder.newLine();
    _builder.append("                     ");
    _builder.append("\'measurement_motor\': Motor(OUTPUT_B),");
    _builder.newLine();
    _builder.append("                     ");
    _builder.append("\'cs_l\': ColorSensor(\'ev3-ports:in1\'), \'cs_m\': ColorSensor(\'ev3-ports:in2\'),");
    _builder.newLine();
    _builder.append("                     ");
    _builder.append("\'cs_r\': ColorSensor(\'ev3-ports:in3\'), \'us_b\': UltrasonicSensor(\'ev3-ports:in4\')}");
    _builder.newLine();
    _builder.append("\n");
    _builder.newLineIfNotEmpty();
    _builder.append("def create_runner():");
    _builder.newLine();
    _builder.append("\t");
    _builder.append("r = Robot(SensorMap(sensor_map_master), bluetooth=BluetoothMaster(MAC_ADDRESS, PORT))");
    _builder.newLine();
    _builder.append("\t");
    _builder.newLine();
    _builder.append("\t");
    {
      EList<Mission> _missions = simulation.getMissions();
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
    _builder.newLine();
    _builder.append("\t");
    _builder.append("Runner(r, [");
    {
      EList<Mission> _missions_1 = simulation.getMissions();
      boolean _hasElements_1 = false;
      for(final Mission m_1 : _missions_1) {
        if (!_hasElements_1) {
          _hasElements_1 = true;
        } else {
          _builder.appendImmediate(", ", "\t");
        }
        _builder.append("mission_");
        String _name = m_1.getName();
        _builder.append(_name, "\t");
      }
    }
    _builder.append("]).run()");
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
    _builder.append("mission_");
    String _name = m.getName();
    _builder.append(_name);
    _builder.append(" = Mission(");
    CharSequence _ActionsToText = PyGenerator.ActionsToText(m.getActions());
    _builder.append(_ActionsToText);
    {
      Celebration _celebration = m.getCelebration();
      boolean _tripleNotEquals = (_celebration != null);
      if (_tripleNotEquals) {
        _builder.append(", ");
        CharSequence _CelebrationToText = PyGenerator.CelebrationToText(m.getCelebration());
        _builder.append(_CelebrationToText);
      }
    }
    _builder.append(")");
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
        Action _get = acts.get((i).intValue());
        int _size_1 = acts.size();
        int _minus = (_size_1 - (i).intValue());
        CharSequence _ActionToText = PyGenerator.ActionToText(_get, _minus);
        _builder.append(_ActionToText);
      }
    }
    _builder.append("]");
    return _builder;
  }
  
  public static CharSequence ActionToText(final Action action, final int default_prio) {
    StringConcatenation _builder = new StringConcatenation();
    String _ActionTypeToString = PyGenerator.ActionTypeToString(action.getType());
    _builder.append(_ActionTypeToString);
    _builder.append("priority=");
    CharSequence _PriorityToText = PyGenerator.PriorityToText(action.getPriority(), default_prio);
    _builder.append(_PriorityToText);
    _builder.append(")");
    return _builder;
  }
  
  public static String ActionTypeToString(final ActionType actionType) {
    if ((actionType instanceof BorderAction)) {
      String _RotationToText = PyGenerator.RotationToText(((BorderAction) actionType).getRotation());
      return ("BorderAction(" + _RotationToText);
    }
    if ((actionType instanceof CollisionAction)) {
      String _RotationToText_1 = PyGenerator.RotationToText(((CollisionAction) actionType).getRotation());
      return ("CollisionAction(" + _RotationToText_1);
    }
    if ((actionType instanceof ColorDetAction)) {
      String _ColorsToText = PyGenerator.ColorsToText(((ColorDetAction) actionType).getColors());
      String _plus = ("ColorDetAction(colors=" + _ColorsToText);
      return (_plus + ", ");
    }
    if ((actionType instanceof DriveAction)) {
      String _SpeedToText = PyGenerator.SpeedToText(((DriveAction) actionType).getSpeed());
      return ("DriveAction(" + _SpeedToText);
    }
    if ((actionType instanceof UltrasoundAction)) {
      String _RotationToText_2 = PyGenerator.RotationToText(((UltrasoundAction) actionType).getRotation());
      String _plus_1 = ("UltrasoundAction(" + _RotationToText_2);
      String _DodgeRocksToText = PyGenerator.DodgeRocksToText(((UltrasoundAction) actionType).getDodgeRocks());
      return (_plus_1 + _DodgeRocksToText);
    }
    if ((actionType instanceof DontDrownAction)) {
      String _ColorsToText_1 = PyGenerator.ColorsToText(((DontDrownAction) actionType).getColors());
      String _plus_2 = ("DontDrownAction(lakes=" + _ColorsToText_1);
      String _plus_3 = (_plus_2 + ", ");
      String _RotationToText_3 = PyGenerator.RotationToText(((DontDrownAction) actionType).getRotation());
      return (_plus_3 + _RotationToText_3);
    }
    if ((actionType instanceof MeasureAction)) {
      String _ColorsToText_2 = PyGenerator.ColorsToText(((MeasureAction) actionType).getColors());
      String _plus_4 = ("MeasureAction(colors=" + _ColorsToText_2);
      return (_plus_4 + ", ");
    }
    if ((actionType instanceof PushRockAction)) {
      int _nr_rocks = ((PushRockAction) actionType).getNr_rocks();
      String _plus_5 = ("PushRockAction(number_of_rocks=" + Integer.valueOf(_nr_rocks));
      return (_plus_5 + ", ");
    }
    return null;
  }
  
  public static String RotationToText(final Rotation r) {
    if ((r != null)) {
      String _rotation = r.getRotation();
      String _plus = ("rotate_degrees=" + _rotation);
      return (_plus + ", ");
    }
    return "";
  }
  
  public static String SpeedToText(final Speed s) {
    if ((s != null)) {
      int _speed = s.getSpeed();
      String _plus = ("speed=" + Integer.valueOf(_speed));
      return (_plus + ", ");
    }
    return "";
  }
  
  public static String DodgeRocksToText(final lego.rover.mission.Boolean b) {
    boolean _equals = Objects.equal(b, lego.rover.mission.Boolean.FALSE);
    if (_equals) {
      return "dodge_rocks=False, ";
    }
    return "";
  }
  
  public static String ColorsToText(final List<Color> colors) {
    String _ColorToText = PyGenerator.ColorToText(colors.get(0));
    String res = ("[" + _ColorToText);
    for (int i = 1; (i < colors.size()); i++) {
      String _res = res;
      String _ColorToText_1 = PyGenerator.ColorToText(colors.get(i));
      String _plus = (", " + _ColorToText_1);
      res = (_res + _plus);
    }
    String _res = res;
    return res = (_res + "]");
  }
  
  public static String ColorToText(final Color color) {
    String _upperCase = color.toString().toUpperCase();
    return ("ColorSensor.COLOR_" + _upperCase);
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
  
  public static CharSequence CelebrationToText(final Celebration celeb) {
    StringConcatenation _builder = new StringConcatenation();
    {
      if ((celeb instanceof DanceCelebration)) {
        _builder.append("DanceCelebration()");
      } else {
        _builder.append("SpeakCelebration(\'");
        String _replace = ((SpeakCelebration) celeb).getToSpeak().replace("\'", "\\\'");
        _builder.append(_replace);
        _builder.append("\')");
      }
    }
    return _builder;
  }
}
