<jsp:useBean id="etalisIO" class="com.etalis.ioEtalis" scope="session" />

<% 
String file = request.getParameter("event_raw")
etalisIO.loadEventFile();

%> 