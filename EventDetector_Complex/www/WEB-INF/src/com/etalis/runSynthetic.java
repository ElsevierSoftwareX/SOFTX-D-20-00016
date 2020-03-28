package com.etalis;

import jpl.Compound;
import jpl.JPL;
import jpl.Query;

public class runSynthetic {
	public String runSyn() {
		JPL.init();
		Query query2 = new Query("consult('C:/Documents and Settings/Administrator/workspace/etalis/src/examples/SynEvents.P')");
		query2.hasSolution();
		Query query3 = new Query("runsyn('C:/Documents and Settings/Administrator/workspace/etalis/src/examples/SynTempStream.P')");
		query3.hasSolution();
		
		Query querylog = new Query("findall(X,time_cpu(X),M)");
		Compound stocklog = (Compound) (querylog.oneSolution().get("M"));
		String tmplog = this.formatString(stocklog.toString());
		//System.out.println(tmplog);
/*		Query queryfired = new Query("findall(X,eventFired(X),L)");
		Compound firedlog = (Compound) (queryfired.oneSolution().get("L"));
		String tmp = this.formatString(firedlog.toString());
		
		return tmp+tmplog;*/
		tmplog = tmplog + "<br>Download the detail log file: <a href=\"download.jsp?filepath=C:\\Documents and Settings\\Administrator\\workspace\\etalis\\src\\examples\\&filename=SynEvent.log \">SynEvent.log</a>";
		return tmplog;
	}
	
	public String runSynnoLog() {
		//
		JPL.init();
		Query query2 = new Query("consult('C:/Documents and Settings/Administrator/workspace/etalis/src/examples/SynEvents_withoutlog.P')");
		query2.hasSolution();
		Query query3 = new Query("runsyn('C:/Documents and Settings/Administrator/workspace/etalis/src/examples/SynTempStream.P')");
		query3.hasSolution();
		
		Query querylog = new Query("findall(X,time_cpu(X),M)");
		Compound stocklog = (Compound) (querylog.oneSolution().get("M"));
		String tmplog = this.formatString(stocklog.toString());
		//System.out.println(tmplog);
/*		Query queryfired = new Query("findall(X,eventFired(X),L)");
		Compound firedlog = (Compound) (queryfired.oneSolution().get("L"));
		String tmp = this.formatString(firedlog.toString());
		
		return tmp+tmplog;*/
		
		return tmplog;
	}
	
	private String formatString(String raw) {
		String tmp = raw;
		tmp = tmp.replaceAll("','", "");
		tmp = tmp.replace(",", "");
		tmp = tmp.replaceAll("'.'", "<br>");
		int gab = tmp.indexOf("[]");
		tmp = tmp.substring(0, gab);

		String tmp1 = "<html><head><link rel=\"stylesheet\" href=\"iframe.css\"></head><body>"+
		"All events from the input stream have been fired.<br>" +
		"The execution has taken: "  + tmp +") sec."  + "</body></html>"		;
		
		return tmp1;		
	}

}
