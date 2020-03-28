package com.etalis;

import jpl.Compound;
import jpl.JPL;
import jpl.Query;
import java.util.Calendar;
import java.util.Scanner;
public class ioEtalis {
	//Properties
	private String inputterm;
	private String inputrules;
	private String etalisStatus;
	private String debuggingMode;
	private String pathToeventFile  ="C:/Documents and Settings/Administrator/workspace/etalis/current_event.event";
	public String Etalislog;
	public String EventsFired;
	public int eventFileLoaded;
	public void init(String EtalisBin) {
		JPL.init();
		String pathToEtalis ="consult('C:/Documents and Settings/Administrator/workspace/etalis/" + EtalisBin;
		Query query1 = new Query("consult('C:/Documents and Settings/Administrator/workspace/etalis/src/event_tr.P')");
		query1.hasSolution();
		query1.close();	
		eventFileLoaded=0;
		
		this.etalisStatus="Engine is running";
	}
	public String status() {
		return this.etalisStatus;
	}
		
	public String query(String quer) {
		// we should either do this via Prolog or java , I think the problem is located in event_tr.P
		/*if (quer.contains("event("));
		{
			Calendar ca = Calendar.getInstance();
			String datime = "datime("+ca.get(Calendar.YEAR)+","+(ca.get(Calendar.MONTH))+","+ca.get(Calendar.DATE)+","+ca.get(Calendar.HOUR_OF_DAY)+","+ca.get(Calendar.MINUTE)+","+ca.get(Calendar.SECOND)+","+ counterTime +")";
		}*/
		Query query1 = new Query(quer);
		query1.hasSolution();
		query1.close();		;
		
		Query queryRule2 =new Query("findall(E,eventFired(E),L)");
		Compound resultEve = (Compound)(queryRule2.oneSolution().get("L"));		
		
		String tmp = resultEve.toString();		
		tmp = this.formatString(tmp);
		this.EventsFired = tmp;
		Query queryRule  =new Query("findall(X,out(X),L)");		
		//queryRule.nextElement();
		Compound result = (Compound)(queryRule.oneSolution().get("L"));
		this.Etalislog = result.toString();
		return this.EventsFired;
	}
	public void basic_query(String quer) {
		Query query1 = new Query(quer);
		query1.hasSolution();
		query1.close();
		
		
	}
	public void query_noOutput(String quer) {
		// we should either do this via Prolog or java , I think the problem is located in event_tr.P
		/*if (quer.contains("event("));
		{
			Calendar ca = Calendar.getInstance();
			String datime = "datime("+ca.get(Calendar.YEAR)+","+(ca.get(Calendar.MONTH))+","+ca.get(Calendar.DATE)+","+ca.get(Calendar.HOUR_OF_DAY)+","+ca.get(Calendar.MINUTE)+","+ca.get(Calendar.SECOND)+","+ counterTime +")";
		}*/
		Query query1 = new Query(quer);
		query1.hasSolution();
		query1.close();
		
		
	}
	public void loadEventFile(String quer) {
	String temp = "compile_events('" + pathToeventFile + "')";
	Query query2 = new Query(temp);
	query2.hasSolution();
	query2.close();
	eventFileLoaded=1;	
	}
	
	//to remove the '.' and [])))
	private String formatString(String raw) {
		String tmp = raw;
		//<div id="outstyle">
		tmp = tmp.replaceAll("','", "");
		tmp = tmp.replaceAll("'.'", "<br>");
		int gab = tmp.indexOf("[]");
		tmp = tmp.substring(0, gab);




		String tmp1 = "<html><head><link rel=\"stylesheet\" href=\"iframe.css\"></head><body>"  + tmp + "</body></html>";
		
		return tmp1;		
	}

}
