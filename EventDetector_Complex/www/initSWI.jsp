<jsp:useBean id="etalisIO" class="com.etalis.ioEtalis" scope="session" />
<% 
	etalisIO.init("etalisIO");
   etalisIO.query("resetProlog.");
   //etalisIO.loadEventFile("C:/Documents and Settings/Administrator/workspace/etalis/default_event.event");

%>