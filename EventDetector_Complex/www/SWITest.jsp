<jsp:useBean id="etalisIO" class="com.etalis.ioEtalis" scope="application" />

<% String content = request.getParameter("eventstream");
response.setContentType("text/html");
response.setHeader("Cache-Control", "no-cache");
String ret   = etalisIO.query(content);
response.getWriter().write(ret); %> 