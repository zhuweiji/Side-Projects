package com.user;

import java.io.*;
import java.nio.file.Path;
import java.util.*;

<<<<<<< HEAD
import com.LogInHandler;
import com.Main;
import com.course.Course;
import com.course.CourseData;
import com.course.Index;
import com.course.IndexData;
import com.course.StudentCourse;
import com.course.StudentCourseData;

public class UserController {
=======
class UserController {
>>>>>>> temp/master
    private final Path datadir = Main.datadir;
    private final Path studentinfopath = Main.studentinfopath;
    private final Path usercredpath = Main.usercredpath;
    private final Path admininfopath = Main.admininfopath;
    private LinkedHashMap<String, String[]> usercredDB = readUserCredDB();
    private UserAcc user;
    public String useridCount; // might have state change if multiple controllers saving to db at once
<<<<<<< HEAD
    public static ArrayList<StudentCourse> studentCourseList = StudentCourseData.studentCourseList;
    public static ArrayList<Course> courseList = CourseData.courseList;
	public static ArrayList<Index> indexList = IndexData.indexList;
	//StudentCourse
	public static ArrayList<StudentCourse> getStudentCourses(){ return studentCourseList; }
	// Course
	public static ArrayList<Course> getCourse(){ return courseList; }
			
	// Index
	public static ArrayList<Index> getIndex(){ return indexList; }
=======
>>>>>>> temp/master

    //singleton design pattern
    private static final UserController instance = new UserController();

    public static UserController getInstance() {
        instance.useridCount = instance.getUserCountFromDB();
        return instance;
    }

    protected UserController() {

    }
    //end singleton pattern

    public void setUser(UserAcc user){
        this.user = user;
    }

    public UserAcc getUser(){
        if (user == null){
            return null;
        }
        return user;
    }

    public UserAcc getNewUserAcc(UserAcc.acc_info acc_info, String permissions){
        return new UserAcc(acc_info, instance.useridCount, permissions);
    }

    public Path getStudentinfopath(){
        return studentinfopath;
    }

    public Path getUsercredpath(){
        return usercredpath;
    }

    public Path getAdmininfopath(){return admininfopath;}

    public void refreshCredDB(){
        usercredDB = readUserCredDB();
    }

    public Path getDatadir() {
        return datadir;
    }

    public String getUseridCount() {
        return useridCount;
    }

    public String getUserCountFromDB(){
        int count = 0;
        try {
            Scanner sc = new Scanner(usercredpath);
            while (sc.hasNextLine()){
                sc.nextLine();
                count++;
            }
            return Integer.toString(count);
        } catch (IOException e) {
<<<<<<< HEAD
            System.out.println("User credentials file not found");
=======
            System.out.println("Print user credentials file not found");
>>>>>>> temp/master
            e.printStackTrace();
        }
        return null;
    }


    HashMap<String, String> readUserInfoDB(Path filepath) {
        File file = new File(filepath.toString());
        HashMap<String, String> userinfo = new HashMap<>();
        try {
            Scanner sc = new Scanner(file);
            while (sc.hasNextLine()) {
                String data = sc.nextLine();
                String[] id_data = data.split(",");
                String[] user_data = Arrays.copyOfRange(id_data, 1, id_data.length);
                String userdata = String.join(",", user_data);
                userinfo.put(id_data[0], userdata);

            }
            return userinfo;
        } catch (FileNotFoundException e) {
            System.out.println(filepath + " file not found in data dir");
            try {
                if (file.createNewFile()) {
                    System.out.println(filepath + " file created");
                    return null;
                } else {
                    System.out.println("File was unable to be created");
                    throw new IOException();
                }
            } catch (IOException f) {
                System.out.println("Fatal IO exception occured while creating file");
                f.printStackTrace();
            }
        }
        return null;
    }
<<<<<<< HEAD
    public LinkedHashMap<String, String[]> readUserCredDB(){
        return LogInHandler.readDB(usercredpath);
    }

    public void pushDB(Path filepath, String[] str, String delimiter, boolean append) throws IOException {
        // appends line
        File file = new File(filepath.toString());
        BufferedWriter writer = new BufferedWriter(new FileWriter(file, append));
        writer.newLine();
        int count=0;
        for (String item: str){
            count++;
            writer.write(item);
            if (count != str.length){
                writer.write(delimiter);
            }

        }
//        writer.newLine();
=======
    LinkedHashMap<String, String[]> readUserCredDB(){
        return LogInHandler.readDB(usercredpath);
    }

    public void pushDB(Path filepath, String[] str, String delimiter) throws IOException {
        File file = new File(filepath.toString());
        BufferedWriter writer = new BufferedWriter(new FileWriter(file, true));
        writer.newLine();
        for (String item: str){
            writer.write(item);
            writer.write(delimiter);
        }
        writer.newLine();
>>>>>>> temp/master
        writer.close();
    }
    public void saveUserCredentials(UserAcc user){
        int count = Integer.parseInt(useridCount);
        count++;
        useridCount=Integer.toString(count);
        String[] useracc_details = {user.getUser_id(),user.getUsername(),user.getSalt(),user.getPassword(),
                user.getHashedPermissions()};
        try {
<<<<<<< HEAD
            pushDB(usercredpath, useracc_details, ",",true);
=======
            pushDB(usercredpath, useracc_details, ",");
>>>>>>> temp/master
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public String[] fetchUserAccDetails(String id){
        String username;
        String[] salt_pw_perm_id;
        for (HashMap.Entry<String, String[]> entry : usercredDB.entrySet()) {
<<<<<<< HEAD
            if (entry.getValue()[0].equals(id)) {
=======
            if (entry.getValue()[4].equals(id)) {
>>>>>>> temp/master
                username = entry.getKey();
                salt_pw_perm_id = entry.getValue();
                String[] result = new String[6];
                result[0] = username;
                System.arraycopy(salt_pw_perm_id, 0, result, 1, salt_pw_perm_id.length); // todo length of array is 5??
                return result;
<<<<<<< HEAD
            }

=======
            } else {
                return null;
            }
        }
        return null;
    }
}

// -------------------------------------------------------------------------------------------------------


class StudentController extends UserController {
    private Student user;
    private final Path studentinfopath = getStudentinfopath();

    private HashMap<String, String> userinfoDB = readUserInfoDB(studentinfopath);
    private String defaultAccessPeriod;

    private static final StudentController instance = new StudentController();

    public StudentController() {
        super();
    }

    public static StudentController getInstance(){
        instance.useridCount = instance.getUserCountFromDB();
        return instance;
    }

    public Student getStudent() {
        return user;
    }

    public void setUser(Student user) {
        this.user = user;
    }



    public Student getNewStudent(){
        Student newstudent = new Student(instance.getUseridCount());
        setUser(newstudent);
        return newstudent;
    }

    public Student getExistingStudent(String username, String hashed_pw, String salt,
                                      String id){
        String[] details = fetchStudentDetails(id);
        UserAcc.acc_info acc_details = new UserAcc.acc_info(username, hashed_pw);
        acc_details.setSalt(salt);
        return new Student(id, details[0], details[1], details[2], details[3], details[4], details[5],
                details[6],details[7],details[8]);


    }

    public String[] fetchStudentDetails(String id) {
        String foo = userinfoDB.get(id);
        if (foo == null){
            return null;
        }
        String[] details = foo.split(",");
        String name = details[0];
        String matricID = details[1];
        String gender = details[2];
        String nationality = details[3];
        String email = details[4];
        String phone_number = details[5];
        String course_of_study = details[6];
        String date_matriculated = details[7];
        String access_period = details[8];

        return details;
    }

    public String fetchStudentUIDFromMatricID(String matricID){
        HashMap<String, String> db = userinfoDB;
        String[] details;
        for (Map.Entry<String, String> entry: db.entrySet()){
            details = entry.getValue().split(",");
            if (details[1].equals(matricID)){
                return entry.getKey();
            }
>>>>>>> temp/master
        }
        return null;
    }

<<<<<<< HEAD
}

// -------------------------------------------------------------------------------------------------------

=======
    public String[] fetchStudentDetailsFromMatricID(String matricID){
        HashMap<String, String> db = userinfoDB;
        String[] details;
        for (Map.Entry<String, String> entry: db.entrySet()){
            details = entry.getValue().split(",");
            if (details[1].equals(matricID)){
                return details;
            }
        }
        return null;
    }


    public void saveStudentToDB(Student student){
        String[] user_details = fetchUserAccDetails(student.getUserid());
        UserAcc user = new UserAcc(user_details[0], user_details[2],user_details[1],user_details[3],user_details[4]);
        saveUserCredentials(user);
        try {
            pushDB(studentinfopath,student.getAllDetails(), ",");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void editExistingStudentInDB(String id, String[] details){

    }

    public void refreshInfoDB(){
        userinfoDB = readUserInfoDB(studentinfopath);
    }


    public void setDefaultAccessPeriod(String accessTime){
        defaultAccessPeriod = accessTime;
        //todo change to Calendar
    }

    public Calendar getDefaultAccessPeriod(){
        return null;
    }

    public String getDefaultStringAccessPeriod(){
        return defaultAccessPeriod;
    }
}
class AdminController extends UserController{
    private Admin user;
    private final Path admininfopath = getAdmininfopath();
    private HashMap<String, String> admininfoDB = readUserInfoDB(admininfopath);

    private static final AdminController instance = new AdminController();

    public AdminController() {
        super();
    }

    public static AdminController getInstance(){
        instance.useridCount = instance.getUserCountFromDB();
        return instance;
    }

    @Override
    public Admin getUser() {
        return user;
    }

    public void setUser(Admin user) {
        this.user = user;
    }

    public Admin getNewAdmin(UserAcc.acc_info acc_details){
        Admin newadmin = new Admin(acc_details, instance.getUseridCount());
        setUser(newadmin);
        return newadmin;
    }

    public Admin getExistingAdmin(String username, String hashed_pw, String salt,
                                  String id){
        String[] admin_info = fetchAdminDetails(id);
        if (admin_info == null){
            return null;
        }
        UserAcc.acc_info acc_details = new UserAcc.acc_info(username, hashed_pw);
        acc_details.setSalt(salt);
        return new Admin(acc_details, id, admin_info[0], admin_info[1], admin_info[2]);
    }

    public String[] fetchAdminDetails(String id){
        String details = admininfoDB.get(id);
        if (details == null){
            System.out.println("couldn't find this user's details in admin details file");
            return null;
        }

        return details.split(",");
    }

    public void refreshAdminInfoDB(){
        admininfoDB = readUserInfoDB(admininfopath);
    }

}
>>>>>>> temp/master
