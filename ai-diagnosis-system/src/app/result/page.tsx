'use client';
import { useRouter } from 'next/router';
import NavLink from "../components/NavLink";
import { useSearchParams } from "next/navigation";
import { useEffect } from 'react';

interface CaseReport {
  id: string;
  title: string;
  explanation: string;
  url: string;
}

const ResultPage = ({ searchParams }: { searchParams: { data?: string } }) => {
  let caseReports: CaseReport[] = [];
      if (searchParams.data) {
        try {
            // Decode and parse the JSON string
            const decodedData = decodeURIComponent(searchParams.data);
            caseReports = JSON.parse(decodedData);
        } catch (error) {
            console.error("Error parsing case reports:", error);
        }
    }
    // do some processing on the data json to get the links
    return (
        <div className="mt-10 mx-auto">
            <h1 className="lg:text-5xl text-3xl font-bold mb-3 text-center">
                Results
            </h1>
            <ol className="mb-3 list-decimal pl-5 ml-4 lg:text-xl text-lg font-normal mt-3">
                {caseReports.map(report => (
                    <li className = "mb-3" key={report.id}>
                        <h1 className="font-bold text-black-500">{report.title}</h1>
                        <p className="lg:text-lg text-sm">{report.explanation}</p>
                        <a href={report.url} className="text-blue-500 hover:underline" target="_blank" rel="noopener noreferrer">View Report</a>
                    </li>
                ))}
            </ol>
           <div className="flex justify-center">
        <NavLink
          href="/start"
          className= "block font-medium text-sm text-white bg-gray-800 hover:bg-gray-600 active:bg-gray-900 md:inline mt-3"
        >
          Try again
        </NavLink>
        </div>
        </div>
    );
};

export default ResultPage;
