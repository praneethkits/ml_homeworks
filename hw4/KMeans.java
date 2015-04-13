/*** Author :Vibhav Gogate
The University of Texas at Dallas
*****/


import java.awt.AlphaComposite;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;
import java.util.*; 

public class KMeans {
    public static void main(String [] args){
	    if (args.length < 3){
	        System.out.println("Usage: Kmeans <input-image> <k> <output-image>");
	        return;
	    }
	    try{
	        BufferedImage originalImage = ImageIO.read(new File(args[0]));
	        int k=Integer.parseInt(args[1]);
	        BufferedImage kmeansJpg = kmeans_helper(originalImage,k);
	        ImageIO.write(kmeansJpg, "jpg", new File(args[2])); 
	    
	    }catch(IOException e){
	        System.out.println(e.getMessage());
	    }	
    }
    
    private static BufferedImage kmeans_helper(BufferedImage originalImage, int k){
	    int w=originalImage.getWidth();
	    int h=originalImage.getHeight();
	    BufferedImage kmeansImage = new BufferedImage(w,h,originalImage.getType());
	    Graphics2D g = kmeansImage.createGraphics();
	    g.drawImage(originalImage, 0, 0, w,h , null);
	    // Read rgb values from the image
	    int[] rgb=new int[w*h];
	    int count=0;
	    for(int i=0;i<w;i++){
	        for(int j=0;j<h;j++){
		        rgb[count++]=kmeansImage.getRGB(i,j);
	        }
	    }
	    // Call kmeans algorithm: update the rgb values
	    kmeans(rgb,k);

	    // Write the new rgb values to the image
	    count=0;
	    for(int i=0;i<w;i++){
	        for(int j=0;j<h;j++){
		        kmeansImage.setRGB(i,j,rgb[count++]);
	        }
	    }
	    return kmeansImage;
    }

    private static class clusteredNode{
    
        public int[] rgb;
        public long error; 
        public clusteredNode(int[] r, long err){
            rgb = r;
            error = err;
        }

    }

    // Your k-means code goes here
    // Update the array rgb by assigning each entry in the rgb array to its cluster center
    private static void kmeans(int[] rgb, int k){

        HashMap<Integer, clusteredNode> mK = new HashMap<Integer, clusteredNode>();
        long outError = Long.MAX_VALUE;
        int minIndex = -1;
        for (int i=0; i<50; i++){
            int[] centroids = new int[k];
            int[] rgbCluster = new int[rgb.length];
            long errorDiff = Integer.MAX_VALUE;
            long error = 0;
            randomInitialize(rgb, centroids);
            while (errorDiff > 100){
                long newError = runKMeans(rgb, centroids, rgbCluster);
                errorDiff = Math.abs(newError - error);
                error = newError;
                System.out.println("Error: " + error + ", errorDiff: " + errorDiff + ", iteration: " + i);
            }
            
            if (error < outError){
                outError = error;
                minIndex = i;
            }
            clusteredNode cN = new clusteredNode(rgbCluster, error);
            mK.put(i, cN);
        }

        clusteredNode cN = mK.get(minIndex);
        copyArray(cN.rgb, rgb);
    }

    private static class node{
        public long rSum;
        public long gSum;
        public long bSum;
        public int count;

        public node(){
            rSum = 0;
            gSum = 0;
            bSum = 0;
            count = 0;
        }
    }

    public static int[] convertRGB(int rgb){
        int [] ret = new int[3];
        ret[0] = (rgb >> 16) & 0xFF;
        ret[1] = (rgb >> 8) & 0xFF;
        ret[2] = rgb & 0xFF;

        return ret;
    }

    public static int getRGB(int r, int g, int b){
        int rgb = ((r << 16) | ((g << 8) | b));
        return rgb;
    }

    public static int getDist(int rgb1, int rgb2){
        int [] rgbValues1 = convertRGB(rgb1);
        int [] rgbValues2 = convertRGB(rgb2);
        int rDist = (rgbValues1[0] - rgbValues2[0])*(rgbValues1[0] - rgbValues2[0]);
        int gDist = (rgbValues1[1] - rgbValues2[1])*(rgbValues1[1] - rgbValues2[1]);
        int bDist = (rgbValues1[2] - rgbValues2[2])*(rgbValues1[2] - rgbValues2[2]);
        int dist = rDist + gDist + bDist;
        return dist;
    }

    public static long runKMeans(int[] rgb, int[] centroids, int[] rgbCluster){

        // printCentroids(centroids);
        long error = 0;
        HashMap<Integer, node> hm = new HashMap<Integer, node>();
        for ( int i = 0; i < rgb.length; i++){
            int minD = Integer.MAX_VALUE;
            // System.out.println("rgb at i is " + rgb[i]);
            for (int j=0; j < centroids.length; j++){
                int dist = getDist(rgb[i], centroids[j]);
                if ( dist < minD){
                    rgbCluster[i] = centroids[j];
                    minD = dist;
                }
            }
            error += minD;

            if (hm.containsKey(rgbCluster[i])){
                node cr = hm.get(rgbCluster[i]);
                int[] rgbValues = convertRGB(rgb[i]);
                cr.rSum += rgbValues[0];
                cr.gSum += rgbValues[1];
                cr.bSum += rgbValues[2];
                cr.count = cr.count + 1;
            }else{
                node cr = new node();
                int[] rgbValues = convertRGB(rgb[i]);
                cr.rSum = rgbValues[0];
                cr.gSum = rgbValues[1];
                cr.bSum = rgbValues[2];
                cr.count = 1;
                hm.put(rgbCluster[i], cr);
            }
        }

        for (int i=0;i<centroids.length; i++){
            //System.out.println(hm.keySet().size());
            System.out.println(hm.keySet());
                node cr = hm.get(centroids[i]);
                int rAvg = (int)cr.rSum/cr.count;
                int gAvg = (int)cr.gSum/cr.count;
                int bAvg = (int)cr.bSum/cr.count;
                centroids[i] = getRGB(rAvg, gAvg, bAvg);
            /*} catch ( Exception e){
                int [] cent =  new int[1];
                randomInitialize(rgb, cent);
                centroids[i] = cent[0];
            }*/
        }

        return error;
    }

    private static void copyArray(int[] src, int[] dest){
         for (int i = 0; i < src.length; i++){
            dest[i] = src[i];
        }
    }

    private static void randomInitialize(int[] rgb, int[] centroids){
        distinctRandomNumbers dRN =  new distinctRandomNumbers(0, rgb.length, centroids.length);
        int[] rands = dRN.getRands();
        for (int i=0; i<rands.length; i++){
            centroids[i] = rgb[rands[i]];
        }
    }

    private static void printCentroids(int[] centroids){
        for (int i=0; i<centroids.length; i++)
            System.out.println("Centroids for " + i + " position = " + centroids[i]);
    }

}
