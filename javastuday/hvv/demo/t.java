import java.io.*;
import java.text.MessageFormat;

public class t {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        String s = new String("rO0ABXVyABNbTGphdmEubGFuZy5PYmplY3Q7kM5YnxBzKWwCAAB4cAAAAAF0AaxSRUV6T0VWRk1Ea3pRVEl5TmpVeFFqWkJNVEV3UVVZd01UbEJOMEpFTlVWRU5VVTBNakkxTWpBelF6aEJNalEwUVRRNU16RkdOa0kzT0RkRk5qVkRNekpHTmprM1FVWXhORE00UmpCRVJUaEROell4T1VRNE9VSkVNRFpGUWpGQ1FqRXhRamxEUVRsQ09VWXpOMEZHUXpOQk5qTTBRelF5TTBRMlF6TTROVFJEUmpFMU5UUXlSVEkwT1VRNVJUSXhNamN4UlVORU5rVXdNMEl3UkVRMVJEazBRMFpDUlRWQ09URTBNak0yUlVFeE1VTTBNek0zUXpWRE5UbEVPREE0UmtJM01qYzNRamd4UmpsRVFUQkJORGxFTmpZeU56ZzNOMFUzTlRKRE1UWXdPVVk1TXpoRU1UZzBNalZCUWtNMFFrSXhSVVZHTlRJMU56WTRRVU14TmpZM1JUTTBPVEJHUXpkRFEwWkRSRGhDUWtRek9Ea3lRakZET0VSRlJETkVRa000UWpJeE1ESXpSVFJEUmpaQk56SkJOalEzTjBRd016SkRNVVkzTkRjPQ==");
        ObjectInputStream ois = new ObjectInputStream(new FileInputStream(
                new File("e:/ooo")));
        Object o =  ois.readObject();

        System.out.println(o.getClass());


    }
}
