<jsp:useBean id="gensyn" class="com.etalis.genEventStream" scope="session"></jsp:useBean>
<html>
<head>
<link rel="stylesheet" href="iframe.css">
</head>
<body>

<%
	String strtmp = request.getParameter("streamsize");
	int streamSize = Integer.parseInt(strtmp);
	
	
	String strtmp1; 
	strtmp1 = request.getParameter("numofparm");
	int numofPar = Integer.parseInt(strtmp1);
	String fileName = "SynTempStream.P";
	gensyn.gen(streamSize,numofPar,fileName);
	String rtn = "Event stream created successfully. To execute the program, press 'Run'.";
	String download = "<br>Download the EventStream source file: <a href=\"download.jsp?filepath=C:\\Documents and Settings\\Administrator\\workspace\\etalis\\src\\examples\\&filename=SynTempStream.P \">SynTempStream.P</a>";
	response.setContentType("text/html");
	response.setHeader("Cache-Control", "no-cache");
	rtn = rtn+download;
	response.getWriter().write(rtn);
%>
</body></html>