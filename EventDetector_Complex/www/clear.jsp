<jsp:useBean id="etalisIO" class="com.etalis.ioEtalis" scope="session" />

<% 
etalisIO.basic_query("retractall(out(_)).");
// here I only want to clear the screen and not remove database data. :-)
response.setContentType("text/html");
response.setHeader("Cache-Control", "no-cache");
response.getWriter().write("cleared");
%> 