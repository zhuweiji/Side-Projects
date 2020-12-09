package com.user;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.HashMap;
import java.util.Scanner;
import java.util.*;


public class LogInHandler {
    private final Path usercredpath = Main.usercredpath;
    private static final LogInHandler instance = new LogInHandler();
    private static final StudentController studentController = StudentController.getInstance();
    private static final AdminController adminController = AdminController.getInstance();
    public static final CommandInterface cmd = CommandInterface.getInstance();
    private UserAcc[] logged_in_users;

    private LogInHandler(){ }

    public static LogInHandler startHandler(){
        return instance;
    }

    public boolean login(String username, String password){
        HashMap<String, String[]> userinfo = readDB(usercredpath);
        String[] id_salt_pw_perm = userinfo.get(username);

        if (id_salt_pw_perm == null){
            return false;
        }

        String hashed_pw = hash(password, id_salt_pw_perm[1]);

        if (hashed_pw.equals(id_salt_pw_perm[2])) {
            if (checkPermissions(id_salt_pw_perm[3], id_salt_pw_perm[1]).equals("student")) {
                cmd.display("Logged in as student");
                StudentInterface studentInterface = StudentInterface.getInstance(username, hashed_pw, id_salt_pw_perm[1],
                id_salt_pw_perm[0]);
                studentInterface.run();
                return true;
            } else if (checkPermissions(id_salt_pw_perm[3], id_salt_pw_perm[1]).equals("admin")) {
                cmd.display("Logged in as admin");
                AdminInterface adminInterface = AdminInterface.getInstance(username, hashed_pw, id_salt_pw_perm[1],
                        id_salt_pw_perm[0]);
                adminInterface.run();
                return true;
            }
                else {
                System.out.println("Permissions are wrong");
                    return false;
            }
        }
        return false;

    }

    public String checkPermissions(String hashed_permissions, String salt){
        if (hash("student", salt).equals(hashed_permissions)){
            return "student";
        }
        else if (hash("admin", salt).equals(hashed_permissions)){
            return "admin";
        }
        return "none";
    }

    public static LinkedHashMap<String, String[]> readDB(Path filepath){
        String delimiter = ",";
        LinkedHashMap<String, String[]> userinfo = new LinkedHashMap<>();

        File file = new File(filepath.toString());
        if (file.length() == 0) {
            return new LinkedHashMap<>();
        }
        try{
            Scanner sc = new Scanner(file);

            while (sc.hasNextLine()){
                String data = sc.nextLine();
                if (data.trim().isEmpty()){
                    break;
                }
                String[] data_split = data.split(delimiter);
                String userid = data_split[0];
                String username = data_split[1];
                String[] id_salt_pw_perm = {userid, data_split[2], data_split[3], data_split[4]};
                userinfo.put(username, id_salt_pw_perm);
            }
            sc.close();
            return userinfo;
        }
        catch (FileNotFoundException e){
            System.out.println("User credentials file not found");
            try {
                if (file.createNewFile()){
                    System.out.println("User credentials file created");
                }
                else{
                    System.out.println("User credentials file was unable to be created.");
                    e.printStackTrace();
                }
            }
            catch (IOException f){
                System.out.println("Userdata file was unable to be created");
                f.printStackTrace();
            }
            return new LinkedHashMap<>();
        }
    }


    public static String hash(String str, String salt){
        //https://www.baeldung.com/java-password-hashing
        try{
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            md.update(salt.getBytes());
            final byte[] hashbytes = md.digest(str.getBytes(StandardCharsets.UTF_8));
            return bytesToHex(hashbytes);
        }
        catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return null;
        }
    }

    private static String bytesToHex(byte[] hash) {
        //https://www.baeldung.com/sha-256-hashing-java
        StringBuilder hexString = new StringBuilder(2 * hash.length);
        for (byte b : hash) {
            String hex = Integer.toHexString(0xff & b);
            if (hex.length() == 1) {
                hexString.append('0');
            }
            hexString.append(hex);
        }
        return hexString.toString();
    }

    public static byte[] getNextSalt() {
        //todo unused here should will be used in admin for generating new users
        byte[] salt = new byte[16];
        Random RANDOM = new SecureRandom();
        RANDOM.nextBytes(salt);
        return salt;
    }

}
