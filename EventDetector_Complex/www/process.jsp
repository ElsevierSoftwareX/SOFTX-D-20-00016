<jsp:useBean id="etalisIO" class="com.etalis.ioEtalis" scope="session" />
<jsp:useBean id="checkInput" class="com.etalis.validateInput" scope="session" />
<% 

String content = request.getParameter("liveQuery");
String option = request.getParameter("logradio");
String ret;
if (checkInput.checkInput(content)) {
	ret = etalisIO.query(content);
	if(option == "raw")
		ret = etalisIO.Etalislog;
	else if (option == "fired")
		ret = etalisIO.EventsFired;

	response.setContentType("text/html");
	response.setHeader("Cache-Control", "no-cache");


	response.getWriter().write(ret);
	
}
else {
	ret = "Your Input:  "+"<span style=\"color: rgb(255, 0, 0);\">"+content+"</span><br>is not valid,Please recheck!";
	response.setContentType("text/html");
	response.setHeader("Cache-Control", "no-cache");


	response.getWriter().write(ret);
}
%> 
