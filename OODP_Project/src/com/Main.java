package com;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.text.*;
import java.io.*;

import com.course.*;

public class Main {
    public static Path cwd;
    public static Path datadir = null;
    public static Path usercredpath;
    public static Path studentinfopath;
    public static Path admininfopath;
    public static Path courseinfopath;
    public static Path indexinfopath;
    public static Path studentcoursepath;
    public static Path lesssonsinfopath;

    public static void main(String[] args)throws ParseException, IOException {

        get_data_paths(false);

        StudentData.initStudents();
		CourseData.initCourses();
		IndexData.initIndex();
		LessonData.initLessons();
		StudentCourseData.initStudentCourses();
        AccountData.initAccounts();


        LogInHandler loginhandler = LogInHandler.startHandler();

        loginhandler.run();
    }
    private static void get_data_paths(boolean visualstudio){
//        if (visualstudio){
//            cwd = Paths.get(System.getProperty("user.dir"),"bin");
//            System.out.println("\n\n\n\n\n");
//            System.out.println(cwd.toString());
//        }
//        else{
//            cwd = Paths.get(System.getProperty("user.dir"));
//        }

//        if (ConsoleUserInterface.getInstance().consoleAvail() && !visualstudio){
//            cwd = cwd.getParent();
//        }
        cwd = Paths.get(System.getProperty("user.dir"));
        if (ConsoleUserInterface.getInstance().consoleAvail()){
            cwd = cwd.getParent();
        }

        datadir = Paths.get(cwd.toString(), "data");
        System.out.println(datadir.toString());

        usercredpath = Paths.get(datadir.toString(), "user_cred.txt");
        studentinfopath = Paths.get(datadir.toString(), "student_info.txt");
        admininfopath = Paths.get(datadir.toString(), "admin_info.txt");
        courseinfopath = Paths.get(datadir.toString(), "Course.txt");
        indexinfopath = Paths.get(datadir.toString(), "Index.txt");
        studentcoursepath = Paths.get(datadir.toString(),"StudentCourse.txt");
        lesssonsinfopath = Paths.get(datadir.toString(), "lessons.txt");
    }


}


