<jsp:useBean id="gfe" class="com.etalis.GoogleFinanceEvent" scope="session" />


<%
	String rtn = gfe.executeEvent("GOOG");
	response.setContentType("text/html");
	response.setHeader("Cache-Control", "no-cache");
	response.getWriter().write(rtn);
%>
