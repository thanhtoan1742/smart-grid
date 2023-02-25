import java.io.*; import java.net.*;
import dk.au.daimi.ascoveco.cpn.engine.Simulator; import dk.au.daimi.ascoveco.cpn.engine.daemon.DaemonSimulator;
import dk.au.daimi.ascoveco.cpn.engine.highlevel.HighLevelSimulator;
import dk.au.daimi.ascoveco.cpn.engine.highlevel.checker.CheckerJob;
import dk.au.daimi.ascoveco.cpn.model.PetriNet; import dk.au.daimi.ascoveco.cpn.model.importer.DOMParser;
public class StateSpaceTool {
public static void main(String[] args) throws Exception {
String file = args[0];
 PetriNet petriNet = DOMParser.parse(new URL("file://" + file));
 HighLevelSimulator s = HighLevelSimulator.getHighLevelSimulator(
 new Simulator(new DaemonSimulator(InetAddress.getLocalHost(), 23456, new File("cpn.ML"))));
 try { CheckerJob checkerJob = new CheckerJob("My model", petriNet, s);
 checkerJob.schedule(); checkerJob.join();
 s.evaluate("use \"simple-dfs.sml\"");
 System.out.println(s.evaluate("let val (s, storage) = dfs dead (CPNToolsModel.getInitialStates())" +
 " in (s, HashTable.numItems storage) " +
 "end"));
 } finally {
 s.destroy();
 } } }