package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;

public final class iodemo_jsp extends org.apache.jasper.runtime.HttpJspBase
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

      out.write("<!--iodemo.jsp-->\r\n");
      out.write("\r\n");
      out.write("<html>\r\n");
      out.write("<head>\r\n");
      out.write("<title>IO Demo</title>\r\n");
      out.write("</head>\r\n");
      out.write("<body>\r\n");
      com.etalis.ioDemo iod = null;
      synchronized (_jspx_page_context) {
        iod = (com.etalis.ioDemo) _jspx_page_context.getAttribute("iod", PageContext.PAGE_SCOPE);
        if (iod == null){
          iod = new com.etalis.ioDemo();
          _jspx_page_context.setAttribute("iod", iod, PageContext.PAGE_SCOPE);
          out.write('\r');
          out.write('\n');
          org.apache.jasper.runtime.JspRuntimeLibrary.introspect(_jspx_page_context.findAttribute("iod"), request);
          out.write('\r');
          out.write('\n');
        }
      }
      out.write("\r\n");
      out.write("\r\n");
      out.write("The following information was saved:\r\n");
      out.write("<ul>\r\n");
      out.write("\t<li> Line1: ");
      out.write(org.apache.jasper.runtime.JspRuntimeLibrary.toString((((com.etalis.ioDemo)_jspx_page_context.findAttribute("iod")).getName())));
      out.write(" </li>\r\n");
      out.write("\t<li> Line2: ");
      out.write(org.apache.jasper.runtime.JspRuntimeLibrary.toString((((com.etalis.ioDemo)_jspx_page_context.findAttribute("iod")).getEmail())));
      out.write(" </li>\r\n");
      out.write("</ul>\r\n");
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
