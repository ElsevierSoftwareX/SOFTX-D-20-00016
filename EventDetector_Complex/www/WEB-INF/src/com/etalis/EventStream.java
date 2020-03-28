package com.etalis;

import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.util.Calendar;
import java.util.Random;
import java.util.Timer;
import java.util.TimerTask;

import jpl.JPL;
import jpl.Query;

public class EventStream {
	private float probabilityValue;
	private int symbol;
	private float price;
	private int volume;
	private float currValue;
	public long counter = 1;
	public long old_counter = 1;
	private Random randGen1 = new Random(); // Default seed comes from system time.
	private Random randGen2 = new Random();
	private Random randGen3 = new Random();
	private Random randGen4 = new Random();
	public double global_duration = 1;
	public EventStream(){}
	
	/**
	 * Generates synthetic event for a given duration time and probability for increasing stock price.
	 * @param duration	- Duration time in seconds (after which the method stops to generate events). If time==0, the method creates infinite event stream;
	 * @param p		- Probability for increasing stock price;
	 * @throws FileNotFoundException 
	 */
	void generateEventStream(double duration, double p)  {
		global_duration = duration;
		Timer counterTimer = new Timer();
		CounterRunner runner = new CounterRunner();
		counterTimer.schedule(runner,0,1000);
		Timer timer = new Timer();
		Stopper stopper = new Stopper();
		timer.schedule(stopper,(long)duration * 1000);
		try {
			 if(p < 0 || p > 1) throw new Exception();
        } catch (Exception e) {
        	System.err.println("Invalid parameter for probability p.");
			e.printStackTrace();
		}
        try{
			/*Increase, decrease or the same value of stocks are created by the following rule, for 0 =< p =< 1:
			if probabilityValue < p increase the stock value;
			if p < probabilityValue < (p+1)/2 decrease the stock value;
			if (p+1)/2 < probabilityValue < 1 the stock value remains the same;*/
			double decr = (p+1)/2;
			Query query=new Query("retractall(logging(on))");
			query.hasSolution();
			while(true){
				BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream("test.P",true)));
				symbol = randGen1.nextInt(2) + 1; // values: 1,2
				price = randGen2.nextInt(1000) + 1; // values: 1,2,...,1000
				volume = randGen3.nextInt(1000) + 1; // values: 1,2,...,1000
				probabilityValue = randGen4.nextFloat(); // values between 0 and 1
				if(probabilityValue < p){
					currValue = increase(price);
				}else if(probabilityValue > p && probabilityValue < decr){
					currValue = decrease(price);
				}else if(probabilityValue > decr){
					currValue = price;
				}
				Calendar ca = Calendar.getInstance();
				//String datime = "datime(" + ca.get(Calendar.YEAR) + "," + ( ca.get(Calendar.MONTH) + 1 ) + "," + ca.get(Calendar.DATE) + "," + ca.get(Calendar.HOUR_OF_DAY) + "," + ca.get(Calendar.MINUTE) + "," + ca.get(Calendar.SECOND) + "," + counter + ")";
				String datime = new String(""+counter);				
				bw.append("event(stock(" + symbol + "," + currValue + "," + volume + "),[" + datime + "," + datime + "])"+".\n");
				//bw.append("event(systemClock(" + datime + "),[" + datime + "," + datime + "])"+".\n");
				//query=new Query("event(stock(" + symbol + "," + currValue + "," + volume + "),[" + datime + "," + datime + "])");
				//query.hasSolution();	
				counter++;
				bw.close();
			}
        } catch (Exception e) {
        	System.err.println("Exception: ");
			e.printStackTrace();
		}
	}
	
	private float increase(float currValue){
		return (float)(currValue + 0.1);
	}
	private float decrease(float currValue){
		return (float)(currValue - 0.1);
	}
	
	class CounterRunner extends TimerTask {
		public void run(){ //Print the number of events generated per second, typically  > 200 000,
			System.out.println("\nNo. of events/second is: " + (counter-old_counter) + ".\n");
			old_counter = counter;
	    }
	}
	class Stopper extends TimerTask {
		public void run(){
			 //Print the number of events generated in total
			System.out.flush();
			System.out.println("\nNo. of events in total is: " + counter + ".");
			System.out.println("No. of total events/second is: " + (counter/global_duration));
			System.out.flush();
			// retrieve the results from Prolog
			//System.out.println("\n  Retrieve the results from Prolog: ");
			//Query queryRule=new Query("findall(eventFired(E),eventFired(E),L)");
			//Compound result = (Compound)(queryRule.oneSolution().get("L"));
			//System.out.println(result);
			System.out.println("Finish.");		
			System.out.flush();
	    	System.exit(0);	// Just stop the execution (it is called after user specified duration).
	    }
	}
	
	public static void main( String argv[]) {
		EventStream stream1 = new EventStream();
		JPL.init(); // create a SWI JPL engine. If you get an exception of jpl not found in your java.library.path then add to your system PATH variable the path: C:\Program Files\pl\bin for Windows or /usr/lib/swi-prolog/lib/i386 for linux
		// JPL for SWI
		Query query=new Query("consult('src/event_tr.P')");
		//Query query=new Query("consult('C:\\Documents and Settings\\danicic\\My Documents\\FZI\\Work\\Work on PhD\\etalis\\etalis\\src\\event_tr.P')");
		query.hasSolution();
		/*Generate a stream of events with probability p = 0.5 and duration = 1 second in the format: stock(Id,Price,Volume) ...*/
		stream1.generateEventStream(35, 0.6);
	}
}
