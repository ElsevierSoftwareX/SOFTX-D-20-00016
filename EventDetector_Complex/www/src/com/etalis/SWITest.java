package com.web.test;


import jpl.Compound;
//import jpl.Term;
//import jpl.Util;
import jpl.JPL;
import jpl.Query;
public class SWITest {
	public String startSWI(String inputStream) {
		JPL.init();
		Query query1 = new Query("consult('E:/workspace/WebTest/prolog_src/event_tr.P')");
		query1.hasSolution();
		query1.close();
		Query query2 = new Query("compile_events('E:/workspace/WebTest/prolog_src/examples/event_test_01.event')");
		query2.hasSolution();
		query2.close();
		Query query3 = new Query(inputStream);
		query3.hasSolution();
		query3.close();
		Query queryRule=new Query("findall(eventFired(event(ce,E)),eventFired(event(ce,E)),L)");
		//queryRule.nextElement();
		Compound result = (Compound)(queryRule.oneSolution().get("L"));
		//Term result = (Term)(queryRule.oneSolution().get("L"));
		return result.toString();
	}

}
