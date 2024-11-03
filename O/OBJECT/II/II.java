import java.util.Scanner;

public class II
{
	double width;
	double height;
	double depth;

	public static void main(String args[])
	{	
		Scanner scanner = new Scanner(System.in);

		II mybox = new II();

		double vol;

		System.out.println("Enter CUBE width: ");
		mybox.width = scanner.nextDouble();

		System.out.println("Enter CUBE height: ");
		mybox.height = scanner.nextDouble();
	
		System.out.println("Enter CUBE depth: ");
		mybox.depth = scanner.nextDouble();
		
		vol = mybox.width * mybox.height * mybox.depth;

		scanner.close();
		System.out.println("Volume is " + vol);
	}
}
