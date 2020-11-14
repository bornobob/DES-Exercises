package lego.rover.validation;

public class Tuple implements Comparable<Object> { 
	public final String x; 
	public final String y; 
	
	public Tuple(String x, String y) { 
	  	this.x = x; 
		this.y = y; 
	}

	@Override
	public int compareTo(Object o) {
		if (!(o instanceof Tuple)) return -1;
		Tuple other = (Tuple)o;
		return this.x.compareTo(other.x);
	} 
} 