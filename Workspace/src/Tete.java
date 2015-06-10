import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

public class Tete {

	public static void main(String[] args) {
		try {
			Process pro2 = Runtime.getRuntime().exec(new String[]{"sh","wget -P /home/hgf/Downloads http://dl.wenku.baidu.com/wenku28/%2Fefcbf95aa70dfef0655e24e43c41001a?sign=MBOT:y1jXjmMD4FchJHFHIGN4z:fEQvX7x7zBb3P8vLNFG%2FPi5QlM8%3D&time=1432000514&amp;response-content-disposition=attachment;%20filename=%22Java%D3%A6%D3%C3%B3%CC%D0%F2%B4%B0%BF%DA%B9%D8%B1%D5%B5%C4%C1%F9%D6%D6%B7%BD%B7%A8.txt%22&response-content-type=application%2foctet-stream"});
			InputStream ins = pro2.getInputStream();
			BufferedReader br = new BufferedReader(new InputStreamReader(ins));
			String line2="";
			System.out.println("进程输出：");
			while((line2 = br.readLine()) != null){
				System.out.println("1");
				System.out.println(line2);
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}

