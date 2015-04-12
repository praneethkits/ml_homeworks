import java.util.*;


public class distinctRandomNumbers {

    private int lowest, highest, noRands;
    
    public distinctRandomNumbers(int n){
        lowest = 0;
        highest = Integer.MAX_VALUE;
        noRands = n;
    }
    
    public distinctRandomNumbers(int s, int b, int n){
        lowest = s;
        highest = b;
        noRands = n;
    }
    
    public distinctRandomNumbers(){
        lowest = 0;
        highest = Integer.MAX_VALUE;
        noRands = 10;
    }
    
    public int[] getRands(){
        int[] ret =  new int[noRands];
        HashMap<Integer, Integer> hm = new HashMap<Integer, Integer>();
        Random rg = new Random();
        int i = 0;
        while (i < noRands){
            int randInt = rg.nextInt(highest);
            randInt += lowest;
            if (hm.containsKey(randInt)){
                continue;
            }else{
                ret[i] = randInt;
                i++;
            }
        }
        return ret;
    }
    
}
