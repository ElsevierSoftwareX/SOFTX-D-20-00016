<!--iodemo.jsp-->
<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<html>
<head>
<title>IO Demo</title>
</head>
<body>
<jsp:useBean id="iod" class="com.etalis.ioDemo" >
<jsp:setProperty property="*" name="iod"/>
</jsp:useBean>

The following information was saved:
<ul>
	<li> Line1: <jsp:getProperty property="name" name="iod"/> </li>
	<li> Line2: <jsp:getProperty property="email" name="iod"/> </li>
</ul>
</body>
</html>