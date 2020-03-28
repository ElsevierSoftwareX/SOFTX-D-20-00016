package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;

public final class ajaxtest_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent {

  private static final JspFactory _jspxFactory = JspFactory.getDefaultFactory();

  private static java.util.List _jspx_dependants;

  private javax.el.ExpressionFactory _el_expressionfactory;
  private org.apache.AnnotationProcessor _jsp_annotationprocessor;

  public Object getDependants() {
    return _jspx_dependants;
  }

  public void _jspInit() {
    _el_expressionfactory = _jspxFactory.getJspApplicationContext(getServletConfig().getServletContext()).getExpressionFactory();
    _jsp_annotationprocessor = (org.apache.AnnotationProcessor) getServletConfig().getServletContext().getAttribute(org.apache.AnnotationProcessor.class.getName());
  }

  public void _jspDestroy() {
  }

  public void _jspService(HttpServletRequest request, HttpServletResponse response)
        throws java.io.IOException, ServletException {

    PageContext pageContext = null;
    HttpSession session = null;
    ServletContext application = null;
    ServletConfig config = null;
    JspWriter out = null;
    Object page = this;
    JspWriter _jspx_out = null;
    PageContext _jspx_page_context = null;


    try {
      response.setContentType("text/html; charset=ISO-8859-1");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("\r\n");
      out.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\" \"http://www.w3.org/TR/html4/loose.dtd\">\r\n");
      out.write("<html>\r\n");
      out.write("<head>\r\n");
      out.write("<script language=\"javascript\" type=\"text/javascript\">\r\n");
      out.write("var xmlHttp = new XMLHttpRequest();\r\n");
      out.write("/* Create a new XMLHttpRequest object to talk to the Web server */\r\n");
      out.write("var xmlHttp = false;\r\n");
      out.write("/*@cc_on @*/\r\n");
      out.write("/*@if (@_jscript_version >= 5)\r\n");
      out.write("try {\r\n");
      out.write("  xmlHttp = new ActiveXObject(\"Msxml2.XMLHTTP\");\r\n");
      out.write("} catch (e) {\r\n");
      out.write("  try {\r\n");
      out.write("    xmlHttp = new ActiveXObject(\"Microsoft.XMLHTTP\");\r\n");
      out.write("  } catch (e2) {\r\n");
      out.write("    xmlHttp = false;\r\n");
      out.write("  }\r\n");
      out.write("}\r\n");
      out.write("@end @*/\r\n");
      out.write("if (!xmlHttp && typeof XMLHttpRequest != 'undefined') {\r\n");
      out.write("  xmlHttp = new XMLHttpRequest();\r\n");
      out.write("}\r\n");
      out.write("function callServer() {\r\n");
      out.write("\t  // Get the city and state from the web form\r\n");
      out.write("\t  var eventstream = document.getElementById(\"eventstream\").value;\r\n");
      out.write("\t  // Only go on if there are values for both fields\r\n");
      out.write("\t  if ((eventstream == null) || (eventstream == \"\")) return;\r\n");
      out.write("\t  // Build the URL to connect to\r\n");
      out.write("\t  var url = \"SWITest.jsp\";\r\n");
      out.write("\t  // Open a connection to the server\r\n");
      out.write("\t  xmlHttp.open(\"GET\", url, true);\r\n");
      out.write("\t  // Setup a function for the server to run when it's done\r\n");
      out.write("\t  xmlHttp.onreadystatechange = updatePage;\r\n");
      out.write("\t  // Send the request\r\n");
      out.write("\t  xmlHttp.send(eventstream);\r\n");
      out.write("\t}\r\n");
      out.write("function updatePage() {\r\n");
      out.write("\t  if (xmlHttp.readyState == 4) {\r\n");
      out.write("\t    var response = xmlHttp.responseText;\r\n");
      out.write("\t    document.getElementById(\"prolog\").value = response;\r\n");
      out.write("\t  }\r\n");
      out.write("\t}\r\n");
      out.write("\r\n");
      out.write("\r\n");
      out.write("</script>\r\n");
      out.write("\r\n");
      out.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=ISO-8859-1\">\r\n");
      out.write("<title>Insert title here</title>\r\n");
      out.write("</head>\r\n");
      out.write("<body>\r\n");
      out.write("<form method = \"get\">\r\n");
      out.write(" <p>EventStream: <input type=\"text\" name=\"eventstream\" id=\"eventstream\" size=\"30\" /></p>\r\n");
      out.write(" <p><input type=\"button\" name=\"trigger\" id=\"trigger\" value=\"trigger\" onclick=\"callServer()\" /></p>\r\n");
      out.write(" </form>\r\n");
      out.write(" <form method = \"get\">\r\n");
      out.write(" <p>return by SWI:<br></br>\r\n");
      out.write(" \t<textarea name=\"prolog\" id=\"prolog\" rows=\"50%\" cols=\"80%\"></textarea>\r\n");
      out.write(" </p>\r\n");
      out.write("</form>\r\n");
      out.write("\r\n");
      out.write("</body>\r\n");
      out.write("</html>");
    } catch (Throwable t) {
      if (!(t instanceof SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          try { out.clearBuffer(); } catch (java.io.IOException e) {}
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
      }
    } finally {
      _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}
