package db;

import java.io.*;
import java.text.*;
import java.util.*;

import uml.Index;

public class IndexData {
	
	@SuppressWarnings("rawtypes")
	public static void write(String fileName, List data) throws IOException {
		PrintWriter out = new PrintWriter(new FileWriter(fileName));

		try {
			for (int i = 0; i < data.size(); i++) {
				out.println((String) data.get(i));
			}
		} finally {
			out.close();
		}
	}

	/** Read the contents of the given file.
	 * 
	 * @param fileName
	 * @return
	 * @throws IOException
	 */
	@SuppressWarnings({ "rawtypes", "unchecked" })
	public static List read(String fileName) throws IOException {
		List data = new ArrayList();
		Scanner scanner = new Scanner(new FileInputStream(fileName));
		try {
			while (scanner.hasNextLine()) {
				data.add(scanner.nextLine());
			}
		} finally {
			scanner.close();
		}
		return data;
	}
	
	public static final String SEPARATOR = "|";
	
	public static ArrayList <Index> indexList = new ArrayList<Index>() ;
	
	/** Initialise the indexes before application starts
     * @param filename
     * @throws IOException
     * @throws ParseException 
     */
@SuppressWarnings({ "rawtypes", "unchecked"})
	
	
	public static ArrayList<Index> initIndexes() throws IOException, ParseException {
		
		// read String from text file
		ArrayList<String> stringArray = (ArrayList) read("src/db/indexes.txt");
		
        for (int i = 0 ; i < stringArray.size() ; i++) {
        	
				String field = (String) stringArray.get(i);
				
				// get individual 'fields' of the string separated by SEPARATOR
				// pass in the string to the string tokenizer using delimiter "," 
				StringTokenizer tokenizer = new StringTokenizer(field, SEPARATOR);	
				
				//first to fifth tokens
				String  courseID = tokenizer.nextToken().trim();	
				int  indexID = Integer.parseInt(tokenizer.nextToken().trim());	
				String tutorialGroup = tokenizer.nextToken().trim();	
				int vacancy = Integer.parseInt(tokenizer.nextToken().trim());
				int waitingList = Integer.parseInt(tokenizer.nextToken().trim());
				
				// create Course object from file data
				Index index = new Index(indexID, courseID, tutorialGroup, vacancy, waitingList);
				// add to Courses list 
				indexList.add(index) ;
		}
		return indexList ;
	}

    /** Initialise the courses before application starts
     * @param filename
     * @throws IOException
     * @throws ParseException 
     */
	@SuppressWarnings({ "rawtypes", "unchecked"})
	public static void searchVacancy(String CourseID,int indexID)throws IOException
	{
		ArrayList<String> stringArray = (ArrayList) read("src/db/index.txt");
		for (int i = 0 ; i < stringArray.size() ; i++) {
        	
			String field = (String) stringArray.get(i);
			
			// get individual 'fields' of the string separated by SEPARATOR
			// pass in the string to the string tokenizer using delimiter "," 
			StringTokenizer tokenizer = new StringTokenizer(field, SEPARATOR);	
			
			//first to fifth tokens
			String  courseID = tokenizer.nextToken().trim();	
			int  indexID1 = Integer.parseInt(tokenizer.nextToken().trim());	
			int vacancy = Integer.parseInt(tokenizer.nextToken().trim());
			
			if(courseID.equalsIgnoreCase(CourseID))
			{
				if(indexID == indexID1)
				System.out.println("Index ID: "+indexID1+" \t Vacancies: "+vacancy);
			}
		}
	}
    /** Initialise the courses before application starts
     * @param filename
     * @throws IOException
     * @throws ParseException 
     */
	@SuppressWarnings({ "rawtypes", "unchecked"})
		public static void showIndex(String CourseID)throws IOException
		{
			ArrayList<String> stringArray = (ArrayList) read("src/db/Index.txt");
			int t=0;
			for (int i = 0 ; i < stringArray.size() ; i++) {
	        	
				String field = (String) stringArray.get(i);
				
				// get individual 'fields' of the string separated by SEPARATOR
				// pass in the string to the string tokenizer using delimiter "," 
				StringTokenizer tokenizer = new StringTokenizer(field, SEPARATOR);	
				
				//first to fifth tokens
				String  courseID = tokenizer.nextToken().trim();	
				String  indexID = tokenizer.nextToken().trim();
				
				if(courseID.equalsIgnoreCase(CourseID))
				{
					
					System.out.println(t+1+") Index ID: "+indexID);
					t++;
				}
			}
	
		}
		
		/** Save the courses that has been added during the session
		 * @param CourseToUpdate
		 * @throws IOException
		 */
		public static void saveIndexes(ArrayList<Index> IndexToUpdate) throws IOException {
			ArrayList <String> cl = new ArrayList<String>() ;// to store Courses data

	        for (int i = 0 ; i < IndexToUpdate.size() ; i++) {
					Index index = (Index) IndexToUpdate.get(i);
					StringBuilder stringBuild =  new StringBuilder() ;
					stringBuild.append(index.getIndexID());
					stringBuild.append(SEPARATOR);
					stringBuild.append(index.getCourseID().trim().toUpperCase());
					stringBuild.append(SEPARATOR);
					stringBuild.append(index.getTutorialGroup().trim().toUpperCase());
					stringBuild.append(SEPARATOR);
					stringBuild.append(index.getVacancy());
					stringBuild.append(SEPARATOR);
					stringBuild.append(index.getWaitingList());

					cl.add(stringBuild.toString()) ;
				}
				write("src/db/index.txt",cl);
		}
}
