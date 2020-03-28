package com.etalis;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.LinkedHashSet;
import java.util.Random;
import java.util.Set;

public class OuOfOrderEventStream {
	public float probabilityValue;
	public int symbol;
	public int counter;
	public int order;
	public int diffEvents;
	public BufferedWriter bw;
	public Random randGen1 = new Random(); 
	public Random randGen2 = new Random();
	public Set<Event> eventStream;
	
	public OuOfOrderEventStream(){}
	
	public static void main( String argv[]) {
		OuOfOrderEventStream stream = new OuOfOrderEventStream();
		try {
			stream.generateEventStream(60000, 0, 6);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * @param streamSize - the size of an event stream to be generated, e.g.,streamSize = 10000, generates 10000 events; 
	 * @param oooPercentage - the percentage of out-of-order events in the stream, e.g., oooPercentage = 0.9, generates a stream with 90% of out-of-order events;
	 * @param diffEvents - the number of events with different id symbols;
	 * @throws IOException
	 */
	void generateEventStream(int streamSize, double oooPercentage, int diffEvents) throws IOException  {
		this.counter = streamSize;
		this.diffEvents = diffEvents;
		this.eventStream = new LinkedHashSet<Event>(streamSize);
		try {
			 if(oooPercentage < 0 || oooPercentage > 1) throw new Exception();
        } catch (Exception e) {
        	System.err.println("Invalid parameter for probability of out-of-order events: oooPercentage.");
			e.printStackTrace();
		}
        Event e;
        boolean duplicate;
        String etalisDir = System.getProperty("user.dir");
        bw = new BufferedWriter(new OutputStreamWriter(
        		//new FileOutputStream(etalisDir + "\\testData\\outOfOrderTest\\test_20000_01_6.P",true)));
        		//new FileOutputStream(etalisDir + "\\testData\\outOfOrderTest\\test_20000_09_6.P",true)));
        		//new FileOutputStream(etalisDir + "\\testData\\outOfOrderTest\\test_40000_09_6.P",true)));
        		//new FileOutputStream(etalisDir + "\\testData\\outOfOrderTest\\test_60000_09_6.P",true)));
        		//new FileOutputStream(etalisDir + "\\testData\\outOfOrderTest\\test_20000_0_6.P",true)));
        		new FileOutputStream(etalisDir + "\\testData\\outOfOrderTest\\test_60000_0_6.P",true)));
        
    	for (int systemClock=1; systemClock<this.counter+1; systemClock++) {
    		symbol = randGen1.nextInt(this.diffEvents) + 1; // values: 1,2,...,diffEvents
    		probabilityValue = randGen2.nextFloat(); // values between 0 and 1
			if(probabilityValue <= oooPercentage){
				// Generate an out-of-order event;
				order = randGen2.nextInt(systemClock); // values: 1,2,...,systemClock-1;
				e = new Event(symbol, order);
			}else {
				// Generate an in-order event;
				e = new Event(symbol, systemClock);
			}
			// Eliminates events with duplicate time points.
			// As the stream is generated at designed time, this iteration is not a performance issue.
			duplicate = false;
			for(Event ev : this.eventStream){
				if(ev.timePoint == e.timePoint){
					this.counter++;
					duplicate = true;
				}
			}
			if(! duplicate){
				this.eventStream.add(e);
				//System.out.println(systemClock + " " + e.toString());
				//System.out.println(e.toString());
			}
        }
    	for(Event ev : this.eventStream){
			bw.append(ev.toString());
		}
        bw.close();
	}
	
	class Event{
		int symbol;
        int timePoint;

        public Event(){};

        public Event(int symbol, int timePoint){
            this.symbol = symbol;
            this.timePoint = timePoint;
        };

        public String toString() {
                StringBuilder buffer = new StringBuilder();
                buffer.append("t"+this.symbol + "([");
                buffer.append(this.timePoint);
                buffer.append(",");
                buffer.append(this.timePoint);
                buffer.append("]).\n");
                
        return buffer.toString();
        }
	}

}
