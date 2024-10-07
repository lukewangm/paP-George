'use client';
import NavLink from "../components/NavLink";
import { useSearchParams } from "next/navigation";

const ResultPage = () => {
    const searchParams = useSearchParams(); // Get search params
    const data = searchParams.get('data'); 

    // do some processing on the data json to get the links
    return (
        <div className="mt-10 mx-auto text-center">
            <h1 className="lg:text-5xl text-3xl font-bold">
                Results
            </h1>
            <p className="mb-3">{JSON.stringify(data)}</p> {/* Display the message directly */}
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
