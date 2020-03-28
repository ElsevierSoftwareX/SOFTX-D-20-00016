<jsp:useBean id="runsyn" class="com.etalis.runSynthetic" scope="session"></jsp:useBean>
<html>
<head>
<link rel="stylesheet" href="iframe.css">
</head>
<body>
<%
String option = request.getParameter("synlog");
String rtn;
if (option.equals("on")) {
	rtn = runsyn.runSyn();
	response.setContentType("text/html");
	response.setHeader("Cache-Control", "no-cache");
	response.getWriter().write(rtn);

}else {
	rtn = runsyn.runSynnoLog();
	
	response.setContentType("text/html");
	response.setHeader("Cache-Control", "no-cache");
	response.getWriter().write(rtn);

}
%>
</body></html>