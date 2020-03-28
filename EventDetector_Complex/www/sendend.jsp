<jsp:useBean id="sendend" class="com.etalis.GoogleFinanceEvent" scope="session" />


<%
	String rtn = sendend.sendStopEvent();
	response.setContentType("text/html");
	response.setHeader("Cache-Control", "no-cache");
	response.getWriter().write(rtn);
%>