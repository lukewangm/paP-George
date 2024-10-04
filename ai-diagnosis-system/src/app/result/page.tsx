'use client';
import { useSearchParams } from "next/navigation";

const ResultPage = () => {
    const searchParams = useSearchParams(); // Get search params
    const data = searchParams.get('data'); 

    return (
        <div>
            <h1>Result</h1>
            <p>{JSON.stringify(data)}</p> {/* Display the message directly */}
        </div>
    );
};

export default ResultPage;
