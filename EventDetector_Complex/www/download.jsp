<%   
     String filename = request.getParameter("filename");//"1a.txt";   
     String filepath = request.getParameter("filepath");//"d:\\";  
     int i = 0;  
     response.setContentType("application/octet-stream");  
     response.setHeader("Content-Disposition","attachment;filename = "+filename);   
     java.io.FileInputStream fileInputStream = new java.io.FileInputStream(filepath+filename);  
     while((i= fileInputStream.read()) != -1){  
     out.write(i);  
    }  
%>  