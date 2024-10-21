'use client';
import NavLink from "../components/NavLink";
import { useSearchParams } from "next/navigation";

const ResultPage = () => {
    const searchParams = useSearchParams(); // Get search params
    const data = searchParams.get('data') || ''; 
    const links = data.split(',');

    // do some processing on the data json to get the links
    return (
        <div className="mt-10 mx-auto text-center">
            <h1 className="lg:text-5xl text-3xl font-bold mb-3">
                Results
            </h1>
            <ul className="mb-3">
              {links.map((link, index) => (
                <li key={index}>
                  <a href={link} className="text-blue-500 hover:underline" target="_blank" rel="noopener noreferrer">
                    {link}
                  </a>
                </li>
              ))}
            </ul>
            
        <NavLink
          href="/start"
          className="block font-medium text-sm text-white bg-gray-800 hover:bg-gray-600 active:bg-gray-900 md:inline mt-3"
        >
          Try again
        </NavLink>
        </div>
    );
};

export default ResultPage;
