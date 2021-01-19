/**
 * generated by Xtext 2.23.0
 */
package lego.rover.generator;

import lego.rover.generator.PyGenerator;
import lego.rover.mission.Missions;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.xtext.generator.AbstractGenerator;
import org.eclipse.xtext.generator.IFileSystemAccess2;
import org.eclipse.xtext.generator.IGeneratorContext;
import org.eclipse.xtext.xbase.lib.IteratorExtensions;

/**
 * Generates code from your model files on save.
 * 
 * See https://www.eclipse.org/Xtext/documentation/303_runtime_concepts.html#code-generation
 */
@SuppressWarnings("all")
public class MissionGenerator extends AbstractGenerator {
  @Override
  public void doGenerate(final Resource resource, final IFileSystemAccess2 fsa, final IGeneratorContext context) {
    EObject _head = IteratorExtensions.<EObject>head(resource.getAllContents());
    final Missions root = ((Missions) _head);
    if ((root != null)) {
      String _lastSegment = resource.getURI().lastSegment();
      String _plus = ("generated/" + _lastSegment);
      String path = (_plus + "/");
      fsa.generateFile((path + "main_main.py"), PyGenerator.ToText(root));
      fsa.generateFile((path + "main_slave.py"), PyGenerator.SlaveToText());
      fsa.generateFile((path + "main.py"), PyGenerator.MainToText());
    }
  }
}
