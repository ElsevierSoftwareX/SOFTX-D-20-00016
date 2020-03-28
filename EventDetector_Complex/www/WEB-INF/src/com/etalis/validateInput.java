package com.etalis;

public class validateInput {

	/**
	 * @param args
	 */
	public boolean checkInput(String inputstream) {
		//
		String tmp = inputstream;
		if (tmp.contains("halt")) return false;
		if (tmp.contains("format")) return false;
		int sleft=0;
		int sright=0;
		for (int i = 0; i < tmp.length(); i++) {
			//
			char ch = tmp.charAt(i);
			if(ch == '(') sleft++;
			else if(ch == ')') sright++;
		}
		if (sleft != sright) return false;
		if (tmp.contains("event("))
			return true;
		else return false;
		//return true;
	}
	
	
	
/*	public static void main(String[] args) {
		// TODO Auto-generated method stub
		validateInput vi = new validateInput();
		if(vi.checkInput("event(a"))
			System.out.println("ok");
		else
			System.out.println("bad");

	}*/

}
