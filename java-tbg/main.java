import java.util.Scanner;

public class main {

    public static boolean compare(String a, String b) {
        return a.compareTo(b) == 0;
    }
   public static void main(String[] args) {
        Scanner my_scanner = new Scanner(System.in);
        String regex = "[,\\s]";
        String path = ".";

        while (true) {
            System.out.print("? ");
            String[] command = my_scanner.nextLine().toLowerCase().strip().split(regex);

            if (command.length == 0) { continue; }

            if(compare(command[0], "ls")) {
                LM_Commands.ls(path);
            }

            if (compare(command[0], "cd")) {
                path += "/" + command[1];
            }

            if (compare(command[0], "pwd")) {
                System.out.println(path);
            }
        }
   }
}
