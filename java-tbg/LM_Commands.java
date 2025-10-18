import java.io.*;

public class LM_Commands {
    public static void ls(String path) {
        File dir = new File(path);
        File[] dir_listing = dir.listFiles();

        if (dir_listing != null) {
            for (File file: dir_listing) {
                System.out.println(file.getName());
            }
        }
    }
}
