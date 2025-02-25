import {Inter, Roboto} from "next/font/google";

export const inter = Inter({
    variable: "--font-inter",
    subsets: ["latin"],
    display: "swap"
  });
  
 export const roboto = Roboto({
    variable: "--font-roboto",
    subsets: ["latin"],
    display: "swap",
    weight: ['100', '300', '400', '500', '700', '900'],
  });