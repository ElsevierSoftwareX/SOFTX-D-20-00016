package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;

public final class process_jsp extends org.apache.jasper.runtime.HttpJspBase
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
      response.setContentType("text/html");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      com.etalis.ioEtalis etalisIO = null;
      synchronized (session) {
        etalisIO = (com.etalis.ioEtalis) _jspx_page_context.getAttribute("etalisIO", PageContext.SESSION_SCOPE);
        if (etalisIO == null){
          etalisIO = new com.etalis.ioEtalis();
          _jspx_page_context.setAttribute("etalisIO", etalisIO, PageContext.SESSION_SCOPE);
        }
      }
      out.write('\n');
      com.etalis.validateInput checkInput = null;
      synchronized (session) {
        checkInput = (com.etalis.validateInput) _jspx_page_context.getAttribute("checkInput", PageContext.SESSION_SCOPE);
        if (checkInput == null){
          checkInput = new com.etalis.validateInput();
          _jspx_page_context.setAttribute("checkInput", checkInput, PageContext.SESSION_SCOPE);
        }
      }
      out.write('\n');
 

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

      out.write(' ');
      out.write('\n');
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
